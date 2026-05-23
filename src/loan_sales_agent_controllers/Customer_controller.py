from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.loan_sales_agent_shared.connection import get_db
from src.loan_sales_agent_BL.schemas.customer_schema import (
CustomerCreate,
CustomerResponse
)
from src.loan_sales_agent_DL.repository.customer_repository import create_customer

router = APIRouter(
    prefix="/customer",
    tags=["customer"]
)

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer_controller(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    new_customer = create_customer(db, customer)
    return new_customer
