import re

from langchain_community.tools import tool
from langchain_core.messages import AIMessage, HumanMessage

from src.agent.states.state import LoanState
from src.loan_sales_agent_DL.repository.customer_repository import get_customer_by_email
from src.loan_sales_agent_shared.connection import AsyncSessionLocal


@tool
async def get_customer_by_email_tool(email_id: str):
    """Fetch a customer by registered email and return CustomerState fields."""
    async with AsyncSessionLocal() as db:
        customer = await get_customer_by_email(db, email_id)

    if not customer:
        return {
            "customer_id": None,
            "customer_verified": False,
        }

    credit_score = None
    if getattr(customer, "credit_score", None) is not None:
        credit_score = customer.credit_score
    elif (
        getattr(customer, "credit_score_rel", None)
        and getattr(customer.credit_score_rel, "credit_score", None)
    ):
        credit_score = customer.credit_score_rel.credit_score.credit_score

    return {
        "customer_id": customer.customer_id,
        "customer_name": customer.name,
        "customer_email": customer.email,
        "credit_score": credit_score,
        "customer_data": {
            "name": customer.name,
            "phone": customer.phone,
            "address": customer.address,
            "city": customer.city,
            "age": customer.age,
        },
        "customer_verified": True,
    }


class VerificationAgent:
    def __init__(self, db=None):
        self.db = db

    def _extract_email(self, text: str) -> str | None:
        match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            text,
        )
        return match.group(0) if match else None

    async def verify_customer(self, state: LoanState) -> dict:
        """Verify customer identity and populate CustomerState fields."""
        if state.get("customer_id"):
            if not state.get("credit_score") and state.get("customer_email"):
                customer_updates = await get_customer_by_email_tool.ainvoke({
                    "email_id": state["customer_email"],
                })
                return {
                    **customer_updates,
                    "customer_verified": True,
                    "next_agent": "underwriting",
                }

            return {
                "customer_verified": True,
                "next_agent": "underwriting",
            }

        last_human_message = next(
            (
                message
                for message in reversed(state.get("messages", []))
                if isinstance(message, HumanMessage)
                or getattr(message, "type", None) == "human"
            ),
            None,
        )

        email_id = None
        if last_human_message:
            email_id = self._extract_email(last_human_message.content)

        if not email_id:
            return {
                "customer_verified": False,
                "next_agent": "verification",
                "messages": [
                    AIMessage(
                        content=(
                            "Please provide your registered email address so "
                            "I can verify your customer profile."
                        )
                    )
                ],
            }

        customer_updates = await get_customer_by_email_tool.ainvoke({
            "email_id": email_id,
        })

        if not customer_updates.get("customer_id"):
            return {
                "customer_email": email_id,
                "customer_verified": False,
                "next_agent": "verification",
                "messages": [
                    AIMessage(
                        content=(
                            "I couldn't find a customer profile for that email. "
                            "Please check the email address and try again."
                        )
                    )
                ],
            }

        return {
            **customer_updates,
            "next_agent": "underwriting",
            "messages": [
                AIMessage(
                    content=(
                        f"Thanks, {customer_updates.get('customer_name')}. "
                        "Your customer profile has been verified."
                    )
                )
            ],
        }

    async def verify_kyc(self, state: LoanState) -> dict:
        customer_data = state.get("customer_data") or {}

        if not customer_data:
            return {
                "kyc_verified": False,
                "messages": [
                    AIMessage(
                        content=(
                            "I couldn't verify your KYC details yet because "
                            "your customer profile is missing."
                        )
                    )
                ],
            }

        return {
            "kyc_verified": True,
            "next_agent": "underwriting",
            "messages": [
                AIMessage(
                    content=(
                        "KYC verification complete.\n\n"
                        f"Name: {customer_data.get('name')}\n"
                        f"Phone: {customer_data.get('phone')}\n"
                        f"Address: {customer_data.get('address')}\n"
                        f"City: {customer_data.get('city')}"
                    )
                )
            ],
        }
