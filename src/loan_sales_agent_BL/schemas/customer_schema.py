from pydantic import BaseModel, EmailStr
from typing import Optional
from decimal import Decimal
from datetime import datetime

from .credit_score_schema import CreditScoreResponse
from .loan_offer_schema import LoanOfferResponse
from .loan_application_schema import LoanApplicationResponse
from .salary_slip_schema import SalarySlipResponse

class CustomerBase(BaseModel):
    name: Optional[str]
    age: Optional[str]
    city: Optional[str]
    phone: str
    address: Optional[str]
    email: EmailStr
    current_loan_amount: Optional[Decimal]
    pre_approved_limit: Optional[Decimal]

class CustomerCreate(CustomerBase):
    password: str

class CustomerResponse(CustomerBase):
    id: str
    created_at: datetime
    updated_at: datetime
    credit_score: Optional[CreditScoreResponse]
    loan_offers: Optional[LoanOfferResponse]
    loan_applications: Optional[LoanApplicationResponse]
    salary_slips: Optional[SalarySlipResponse]