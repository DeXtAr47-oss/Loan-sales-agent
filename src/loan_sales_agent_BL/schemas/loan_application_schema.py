from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

from .salary_slip_schema import SalarySlipResponse

class LoanApplicationBase(BaseModel):
    loan_amount: Decimal
    tenure_months: int
    interest_rate: Decimal
    monthly_emi: int
    status: Optional[str]
    rejection_reason: Optional[str]

class LoanApplicationCreate(LoanApplicationBase):
    conversation_id: Optional[str]
    conversation_history: Optional[List[str]] = []

class LoanApplicationResponse(LoanApplicationBase):
    application_id: int
    customer_id: int
    conversation_id: int
    created_at: datetime
    approved_at: datetime
    salary_slips: List[SalarySlipResponse] = []

    class Config:
        orm_mode = True