from decimal import Decimal
import json
from typing import Optional

from langchain.agents import create_agent
from langchain_community.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from src.loan_sales_agent_shared.config import LLM
from src.agent.states.state import LoanState
from src.loan_sales_agent_DL.repository.loan_offer_repository import get_loan_offers
from src.loan_sales_agent_shared.connection import AsyncSessionLocal


class LoanRequirements(BaseModel):
    loan_type: Optional[str] = Field(
        default=None,
        description="The type or purpose of the loan stated by the customer.",
    )
    loan_amount: Optional[Decimal] = Field(
        default=None,
        description="Requested loan amount in Indian rupees as a plain numeric value.",
    )
    tenure_months: Optional[int] = Field(
        default=None,
        description="Requested repayment tenure converted to months.",
    )


@tool
async def loan_offers():
    """
    Fetch active loan offers from the database.
    Returns the available amount range, interest rate, and tenure for each offer.
    """
    async with AsyncSessionLocal() as db:
        offers = await get_loan_offers(db)
        if not offers:
            return {
                "summary": "No active loan offers found.",
                "offers": [],
            }

        lines = [f"Found {len(offers)} loan offer(s):"]
        offer_rows = []
        for offer in offers:
            lines.append(
                f"ID: {offer.offer_id} | "
                f"Amount: ₹{offer.amount_range_min:,.0f}–"
                f"₹{offer.amount_range_max:,.0f} | "
                f"Rate: {offer.interest_rate}% | "
                f"Tenure: {offer.tenure_months} months"
            )
            offer_rows.append({
                "loan_offer_id": offer.offer_id,
                "amount_range_min": str(offer.amount_range_min),
                "amount_range_max": str(offer.amount_range_max),
                "interest_rate": str(offer.interest_rate),
                "tenure_months": offer.tenure_months,
            })

        return {
            "summary": "\n".join(lines),
            "offers": offer_rows,
        }


class SalesAgent:
    def __init__(self):
        self.llm = LLM

    def _has_sales_value(self, value):
        return value not in (None, "", 0, Decimal("0"))

    def _is_affirmative(self, text: str) -> bool:
        normalized_text = text.strip().lower()
        affirmative_phrases = {
            "yes",
            "yes please",
            "yeah",
            "yep",
            "sure",
            "ok",
            "okay",
            "proceed",
            "continue",
            "i want to proceed",
            "go ahead",
        }
        return (
            normalized_text in affirmative_phrases
            or "proceed" in normalized_text
            or "go ahead" in normalized_text
        )

    def _format_offer_message(self, offer: dict) -> str:
        return (
            "I found a matching loan offer for you:\n\n"
            f"- Offer ID: {offer['loan_offer_id']}\n"
            f"- Eligible amount range: ₹{Decimal(str(offer['amount_range_min'])):,.0f} "
            f"to ₹{Decimal(str(offer['amount_range_max'])):,.0f}\n"
            f"- Interest rate: {offer['interest_rate']}%\n"
            f"- Tenure: {offer['tenure_months']} months\n\n"
            "Would you like to proceed with this loan offer?"
        )

    def _parse_requirements_json(self, content: str) -> LoanRequirements:
        """Parse the JSON object returned by the local LLM."""
        cleaned_content = content.strip()
        if cleaned_content.startswith("```"):
            cleaned_content = cleaned_content.strip("`").strip()
            if cleaned_content.startswith("json"):
                cleaned_content = cleaned_content[4:].strip()

        object_start = cleaned_content.find("{")
        object_end = cleaned_content.rfind("}")
        if object_start == -1 or object_end == -1:
            return LoanRequirements()

        try:
            parsed = json.loads(cleaned_content[object_start:object_end + 1])
        except json.JSONDecodeError:
            return LoanRequirements()

        return LoanRequirements.model_validate(parsed)

    async def _get_matching_loan_offer(self, loan_amount, tenure_months):
        """Use the loan_offers tool to derive loan_offer_id and pre_approved_limit."""
        if not self._has_sales_value(loan_amount):
            return {}, None

        tool_result = await loan_offers.ainvoke({})
        offers = tool_result.get("offers", []) if isinstance(tool_result, dict) else []
        loan_amount = Decimal(str(loan_amount))

        matching_offers = [
            offer
            for offer in offers
            if (
                Decimal(str(offer["amount_range_min"]))
                <= loan_amount
                <= Decimal(str(offer["amount_range_max"]))
            )
        ]

        if tenure_months:
            tenure_matches = [
                offer
                for offer in matching_offers
                if offer["tenure_months"] == tenure_months
            ]
            if tenure_matches:
                matching_offers = tenure_matches

        if not matching_offers:
            return {}, None

        selected_offer = matching_offers[0]
        return (
            {
                "loan_offer_id": selected_offer["loan_offer_id"],
                "pre_approved_limit": Decimal(str(selected_offer["amount_range_max"])),
                "next_agent": "sales",
            },
            selected_offer,
        )

    async def collect_requirements(self, state: LoanState) -> tuple[dict, list[str], Optional[str]]:
        """Extract requirements from the latest customer message and report missing fields."""
        last_human_message = next(
            (
                message
                for message in reversed(state.get("messages", []))
                if isinstance(message, HumanMessage)
                or getattr(message, "type", None) == "human"
            ),
            None,
        )

        current_values = {
            "loan_type": state.get("loan_type") or None,
            "loan_amount": state.get("loan_amount") or None,
            "tenure_months": state.get("tenure_months") or None,
            "loan_offer_id": state.get("loan_offer_id") or None,
            "pre_approved_limit": state.get("pre_approved_limit") or None,
        }

        if (
            self._has_sales_value(current_values.get("loan_offer_id"))
            and self._has_sales_value(current_values.get("pre_approved_limit"))
            and state.get("next_agent") == "sales"
            and last_human_message
        ):
            if self._is_affirmative(last_human_message.content):
                return (
                    {"next_agent": "verification"},
                    [],
                    "Great, let's proceed with this loan offer. I’ll verify your customer profile now.",
                )

            return (
                {"next_agent": "sales"},
                [],
                "Please reply with yes if you want to proceed with this loan offer.",
            )

        updates = {}
        if last_human_message:
            try:
                response = await self.llm.ainvoke([
                    SystemMessage(content=(
                        "Extract loan requirements from the customer's message.\n\n"
                        "Return ONLY valid JSON in this exact format:\n"
                        "{\n"
                        '  "loan_type": null,\n'
                        '  "loan_amount": null,\n'
                        '  "tenure_months": null\n'
                        "}\n\n"
                        "Rules:\n"
                        "- Do not guess missing values.\n"
                        "- Convert lakh/lac to rupees. Example: 5 lakh = 500000.\n"
                        "- Convert crore/cr to rupees. Example: 1 crore = 10000000.\n"
                        "- Convert years to months. Example: 2 years = 24.\n"
                        "- Use null for values not stated by the customer.\n"
                        "- Do not include markdown, comments, or explanation."
                    )),
                    HumanMessage(content=last_human_message.content),
                ])
                extracted = self._parse_requirements_json(response.content)
            except Exception:
                extracted = LoanRequirements()

            if extracted.loan_type:
                updates["loan_type"] = extracted.loan_type
            if extracted.loan_amount and extracted.loan_amount > 0:
                updates["loan_amount"] = extracted.loan_amount
            if extracted.tenure_months and extracted.tenure_months > 0:
                updates["tenure_months"] = extracted.tenure_months

        merged_values = {**current_values, **updates}
        customer_required_fields = [
            "loan_type",
            "loan_amount",
            "tenure_months",
        ]
        missing_customer_fields = [
            field_name
            for field_name in customer_required_fields
            if not self._has_sales_value(merged_values.get(field_name))
        ]
        if missing_customer_fields:
            return updates, missing_customer_fields, None

        if (
            self._has_sales_value(merged_values.get("loan_type"))
            and self._has_sales_value(merged_values.get("loan_amount"))
            and self._has_sales_value(merged_values.get("tenure_months"))
            and (
                not self._has_sales_value(merged_values.get("loan_offer_id"))
                or not self._has_sales_value(merged_values.get("pre_approved_limit"))
            )
        ):
            offer_updates, selected_offer = await self._get_matching_loan_offer(
                merged_values["loan_amount"],
                merged_values["tenure_months"],
            )
            updates.update(offer_updates)
            merged_values = {**merged_values, **offer_updates}
            if selected_offer:
                return updates, [], self._format_offer_message(selected_offer)

        sales_state_fields = [
            "loan_type",
            "loan_amount",
            "tenure_months",
            "loan_offer_id",
            "pre_approved_limit",
        ]
        missing_fields = [
            field_name
            for field_name in sales_state_fields
            if not self._has_sales_value(merged_values.get(field_name))
        ]

        if not missing_fields:
            updates["next_agent"] = "sales"

        return updates, missing_fields, None

    def create_sales_agent(self):
        llm_with_tools = self.llm.bind_tools(
            [loan_offers],
            tool_choice="any",  # "any" = MUST call a tool, "auto" = optional
        )

        return create_agent(
            model=llm_with_tools,
            tools=[loan_offers],
            system_prompt=(
                "You are a sales agent. You have one tool: loan_offers.\n\n"
                "WHEN TO USE:\n"
                "- User asks about loans → call loan_offers IMMEDIATELY\n"
                "- User asks about interest rates → call loan_offers\n"
                "- User asks about banks → call loan_offers\n\n"
                "HOW TO USE:\n"
                "1. Call the tool. Do not explain that you are calling it.\n"
                "2. Wait for the tool result.\n"
                "3. Return the result to the supervisor.\n\n"
                "NEVER output the tool name as plain text. Always invoke it."
            ),
            name="sales_agent",
        )
