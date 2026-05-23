from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import EmailStr
from typing import List
import uuid

from src.loan_sales_agent_shared.connection import get_db
from src.loan_sales_agent_BL.schemas.customer_schema import (
CustomerCreate,
CustomerResponse
)
from src.loan_sales_agent_BL.services.customer_service import (
get_all_customer_service,
get_by_email_customer_service,
get_by_id_customer_service,
create_customer_service,
update_customer_service,
delete_customer_service
)

router = APIRouter(
    prefix="/customer",
    tags=["customer"]
)

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer_controller(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    new_customer = create_customer_service(db, customer)
    return new_customer

@router.get("/", response_model=List[CustomerResponse], status_code=status.HTTP_200_OK)
def get_all(db: Session = Depends(get_db)):
    return get_all_customer_service(db)

@router.get("/{customer_id}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
def get_id(
    customer_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    return get_by_id_customer_service(db, customer_id)

@router.get("/email/{customer_email}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
def get_email(
        customer_email: EmailStr,
        db: Session = Depends(get_db)
):
    return get_by_email_customer_service(db, customer_email)

@router.put("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def update(
        customer_id: uuid.UUID,
        customer: CustomerCreate,
        db: Session = Depends(get_db)
):
    update_customer_service(db, customer_id, customer)
    return {"message": "customer updated"}


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(customer_id: uuid.UUID, db: Session = Depends(get_db)):
    delete_customer_service(db, customer_id)
    return {"message": "customer deleted"}
