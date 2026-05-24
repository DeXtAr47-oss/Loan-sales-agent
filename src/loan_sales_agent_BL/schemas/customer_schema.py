from pydantic import BaseModel, EmailStr
from typing import Optional
from decimal import Decimal
from datetime import datetime
import uuid

from .credit_score_schema import CreditScoreResponse
from .loan_offer_schema import LoanOfferResponse
from .loan_application_schema import LoanApplicationResponse
from .salary_slip_schema import SalarySlipResponse

class CustomerBase(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    city: Optional[str] = None
    phone: str = None
    address: Optional[str] = None
    email: EmailStr = None
    credit_score: Optional[int] = None
    current_loan_amount: Optional[Decimal] = None
    pre_approved_limit: Optional[Decimal] = None

class CustomerCreate(CustomerBase):
    password: str = None

class CustomerResponse(CustomerBase):
    customer_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    credit_score: Optional[CreditScoreResponse] = None
    loan_offers: Optional[LoanOfferResponse] = None
    loan_applications: Optional[LoanApplicationResponse] = None
    salary_slips: Optional[SalarySlipResponse] = None