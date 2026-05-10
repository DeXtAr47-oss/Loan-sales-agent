from typing import TypedDict, Annotated, Optional
from decimal import Decimal
import operator

class LoanState(TypedDict):
    
    # conversation
    messages: Annotated[list, operator.add]
    conversation_id: str 

    # Customer info
    customer_id: int
    customer_name: Optional[str]
    customer_email: Optional[str]
    customer_data: Optional[dict]
    customer_verified: Optional[bool]

    # Loan details
    loan_amount: Decimal
    loan_type: str
    tenure_months: int
    interest_rate: Decimal
    monthly_emi: Decimal

    # process flags
    kyc_verified: bool
    credit_check_done: bool
    under_writing_approved: bool
    salary_slip_uploaded: bool
    salary_amount: Optional[float]

    # Decission
    pre_approved_limit: Optional[Decimal]
    credit_score: Optional[int]
    application_id: Optional[str]
    final_status: Optional[str]
    rejection_reason: Optional[str]
    sanction_letter_path: Optional[str]

    # Flow control
    next_action: Optional[str]
