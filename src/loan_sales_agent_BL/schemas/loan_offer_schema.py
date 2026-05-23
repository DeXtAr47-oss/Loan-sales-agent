from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class LoanOfferBase(BaseModel):
    amount_range_min: Decimal
    amount_range_max: Decimal
    interest_rate: Decimal
    tenure_months: int

class LoanOfferCreate(LoanOfferBase):
    pass

class LoanOfferResponse(LoanOfferBase):
    offer_id: int
    created_at: datetime

    class Config:
        from_attributes = True