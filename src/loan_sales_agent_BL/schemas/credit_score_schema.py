from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreditScoreBase(BaseModel):
    credit_score: int

class CreditScoreCreate(CreditScoreBase):
    pass

class CreditScoreResponse(CreditScoreBase):
    credit_score_id: int
    last_updated: Optional[datetime]

    class Config:
        from_attributes = True