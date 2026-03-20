from pydantic import BaseModel, EmailStr
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

from .models import Customer, CreditScore, LoanApplication, LoanOffer, SalarySlip

# CREDIT SCORE
class CreditScoreBase(BaseModel):
    credit_score: int

class CreditScoreCreate(CreditScoreBase):
    pass

class CreditScoreResponse(CreditScoreBase):
    customer_id: int
    last_updated: datetime

    class Config:
        orm_mode = True


# SALARY SLIP
class SalarySlipBase(BaseModel):
    monthly_salary: Decimal
    file_path: Optional[str]

class SalarySlipCreate(SalarySlipBase):
    application_id: int


class SalarySlipResponse(SalarySlipBase):
    slip_id: str
    customer_id: int
    application_id: int
    upload_date: datetime

    class Config:
        orm_mode = True

#LOAN OFFERS
class LoanOfferBase(BaseModel):
    amount_range_min: Decimal
    amount_range_max: Decimal
    interest_rate: Decimal
    tenure_months: int

class LoanOfferCreate(LoanOfferBase):
    pass

class LoanOfferResponse(LoanOfferBase):
    offer_id: int
    customer_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# LOAN APPLICATION
class LoanApplicationBase(BaseModel):
    loan_amount: Decimal
    tenure_months: int
    interest_rate: Decimal
    monthly_emi: int
    status: Optional[str]
    rejection_reason: Optional[str]

class LoanApplicationCreate(LoanApplicationBase):
    conversation_id: Optional[str]

class LoanApplicationResponse(LoanApplicationBase):
    application_id: int
    customer_id: int
    conversation_id: int
    created_at: datetime
    approved_at: datetime
    salary_slips: List[SalarySlipResponse] = []

    class Config:
        orm_mode = True

# CUSTOMER
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
    id: int
    created_at: datetime
    updated_at: datetime
    credit_score: Optional[CreditScoreResponse]
    loan_offers: Optional[LoanOfferResponse]
    loan_applications: Optional[LoanApplicationResponse]
    salary_slips: Optional[SalarySlipResponse]    