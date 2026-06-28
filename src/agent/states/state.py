from decimal import Decimal
from typing import Annotated, Optional, TypedDict
from uuid import UUID

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class ConversationState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    conversation_id: UUID
    next_agent: Optional[str]


class CustomerState(TypedDict, total=False):
    customer_id: Optional[UUID]
    customer_name: Optional[str]
    customer_email: Optional[str]
    customer_data: Optional[dict]
    credit_score: Optional[int]
    customer_verified: bool


class SalesAgentState(TypedDict, total=False):
    loan_type: Optional[str]
    loan_amount: Optional[Decimal]
    tenure_months: Optional[int]
    pre_approved_limit: Optional[Decimal]

    # selected / returned loan offer state
    loan_offer_id: Optional[int]


class VerificationAgentState(TypedDict, total=False):
    kyc_verified: bool


class UnderwritingAgentState(TypedDict, total=False):
    interest_rate: Optional[Decimal]
    monthly_emi: Optional[Decimal]
    credit_check_done: bool
    under_writing_approved: bool
    salary_slip_uploaded: bool
    salary_slip_path: Optional[str]
    salary_slip_date: Optional[str]
    salary_amount: Optional[float]
    pre_approved_limit: Optional[Decimal]
    credit_score: Optional[int]
    final_status: Optional[str]
    rejection_reason: Optional[str]


class SanctionAgentState(TypedDict, total=False):
    application_id: Optional[str]
    sanction_letter_path: Optional[str]
    sanction_letter_url: Optional[str]


class MasterAgentState(
    ConversationState,
    CustomerState,
):
    pass


class LoanState(
    ConversationState,
    CustomerState,
    SalesAgentState,
    VerificationAgentState,
    UnderwritingAgentState,
    SanctionAgentState,
):
    pass
