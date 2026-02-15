from typing import TypedDict, Annotated, Optional
import operator

class LoanState(TypedDict):
    
    # conversation
    messages: Annotated[list, operator.add]
    conversation_id: str 

    # Customer info
    customer_id: Optional[str]
    customer_name: Optional[str]
    customer_email: Optional[str]
    customer_data: Optional[dict]

    # Loan details
    loan_amount: Optional[float]
    tenure_months: Optional[int]
    interest_rate: Optional[float]
    monthly_emi: Optional[float]

    # process flags
    kyc_verified: bool
    credit_check_done: bool
    under_writing_approved: bool
    salary_slip_uploaded: bool
    salary_amount: Optional[float]

    # Decission
    pre_approved_limit: Optional[float]
    credit_score: Optional[int]
    application_id: Optional[str]
    final_status: Optional[str]
    rejection_reason: Optional[str]
    sanction_letter_path: Optional[str]

    # Flow control
    next_action: Optional[str]
