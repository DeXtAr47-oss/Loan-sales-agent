from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class LoanOfferBase(BaseModel):
    amount_range_min: Decimal | None = None
    amount_range_max: Decimal | None = None
    interest_rate: Decimal | None = None
    tenure_months: int | None = None

class LoanOfferRequest(LoanOfferBase):
    pass

class LoanOfferResponse(LoanOfferBase):
    offer_id: int
    created_at: datetime

    class Config:
        from_attributes = True