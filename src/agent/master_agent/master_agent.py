import uuid
from langchain.agents import create_agent
from langchain.messages import SystemMessage, AIMessage, HumanMessage
from typing import Literal

from src.loan_sales_agent_shared.config import LLM
from src.agent.sales_agent.sales_agent import SalesAgent
from src.agent.states.state import LoanState

class MasterAgent:
    def __init__(self):
        self.llm = LLM
        self.sales_agent_instance = SalesAgent()
        self.sales_agent = self.sales_agent_instance.create_sales_agent()

    async def supervisor_node(self, state: LoanState):
        """Router node — decides where to send the request. Does NOT add routing noise to messages."""
        messages = state["messages"]

        # Continue an in-progress verification flow across turns.
        if state.get("next_agent") == "verification" and not state.get("customer_verified"):
            return {"next_agent": "verification"}

        # Continue an in-progress underwriting/salary-slip flow across turns.
        if state.get("next_agent") == "underwriting":
            return {"next_agent": "underwriting"}

        if state.get("next_agent") == "sanction":
            return {"next_agent": "sanction"}

        # Continue an in-progress sales offer confirmation across turns.
        if state.get("next_agent") == "sales" and state.get("loan_offer_id"):
            return {"next_agent": "sales"}

        # Only route if there's an actual user message
        if not messages:
            return {"next_agent": "end"}

        # Get last user message for routing
        last_user_msg = None
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage) or getattr(msg, "type", None) == "human":
                last_user_msg = msg
                break

        if not last_user_msg:
            return {"next_agent": "direct"}

        # Routing prompt — NOT stored in messages
        routing_prompt = SystemMessage(content=(
            "You are a router. Analyze the user's request and respond with EXACTLY one word:\n"
            "'sales' - for loan offers, interest rates, bank comparisons, EMI calculations\n"
            "'direct' - for greetings, chitchat, or general questions not related to loans\n"
            "Respond with only the label, nothing else."
        ))

        response = await self.llm.ainvoke([routing_prompt, last_user_msg])
        decision = response.content.strip().lower()

        # Return routing decision WITHOUT adding to messages
        return {"next_agent": decision}

    async def sales_node(self, state: LoanState):
        """Delegates to the sales agent."""
        updates, missing_fields, sales_reply = await self.sales_agent_instance.collect_requirements(state)

        if sales_reply:
            return {
                **updates,
                "messages": [AIMessage(content=sales_reply)],
            }

        if missing_fields:
            system_derived_fields = {"loan_offer_id", "pre_approved_limit"}
            if system_derived_fields.intersection(missing_fields):
                return {
                    **updates,
                    "messages": [
                        AIMessage(
                            content=(
                                "I couldn't find a matching loan offer for the "
                                "amount and tenure you provided. Please try a "
                                "different loan amount or tenure."
                            )
                        )
                    ],
                }

            field_labels = {
                "loan_type": "loan type",
                "loan_amount": "desired loan amount",
                "tenure_months": "preferred tenure",
            }
            missing_labels = [field_labels[field] for field in missing_fields]
            if len(missing_labels) == 1:
                requested_details = missing_labels[0]
            else:
                requested_details = (
                    ", ".join(missing_labels[:-1]) + f" and {missing_labels[-1]}"
                )

            return {
                **updates,
                "messages": [
                    AIMessage(
                        content=f"Please provide your {requested_details} so I can find the right loan offer."
                    )
                ],
            }

        return {
            **updates,
            "messages": [
                AIMessage(
                    content="I have the loan details. Would you like to proceed?"
                )
            ],
        }

    async def direct_node(self, state: LoanState):
        """Handles general queries directly."""
        # Prepend system context for direct responses
        system_msg = SystemMessage(content="You are a helpful loan sales agent answer only to loan related questions except nothing else.")
        response = await self.llm.ainvoke([system_msg] + state["messages"])
        return {"messages": [response]}

    def route(self, state: LoanState) -> Literal["sales", "verification", "underwriting", "sanction", "direct", "end"]:
        next_agent = state.get("next_agent", "direct")
        if next_agent == "sales":
            return "sales"
        elif next_agent == "verification":
            return "verification"
        elif next_agent == "underwriting":
            return "underwriting"
        elif next_agent == "sanction":
            return "sanction"
        elif next_agent == "direct":
            return "direct"
        return "end"

    def route_after_sales(self, state: LoanState) -> Literal["verification", "end"]:
        if state.get("next_agent") == "verification":
            return "verification"
        return "end"

    def route_after_verification(self, state: LoanState) -> Literal["underwriting", "end"]:
        if state.get("next_agent") == "underwriting":
            return "underwriting"
        return "end"

    def route_after_underwriting(self, state: LoanState) -> Literal["sanction", "end"]:
        if state.get("next_agent") == "sanction":
            return "sanction"
        return "end"
