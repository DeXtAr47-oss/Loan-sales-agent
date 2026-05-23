from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class SalarySlipBase(BaseModel):
    monthly_salary: Decimal
    file_path: Optional[str]

class SalarySlipCreate(SalarySlipBase):
    application_id: int


class SalarySlipResponse(SalarySlipBase):
    slip_id: str
    application_id: int
    upload_date: datetime

    class Config:
        from_attributes = True