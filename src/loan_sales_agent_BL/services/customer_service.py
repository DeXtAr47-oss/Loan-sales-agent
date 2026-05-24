from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from pydantic import EmailStr
import uuid

from src.loan_sales_agent_BL.schemas.customer_schema import CustomerCreate, CustomerBase
from src.loan_sales_agent_DL.repository.customer_repository import (
    get_all_customer,
    get_customer_by_id,
    get_customer_by_email,
    create_customer,
    update_customer,
    delete_customer,
    check_email,
    check_phone_number
)

def get_all_customer_service(db: Session):
    customers = get_all_customer(db)
    if customers is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customers not found")
    return customers

def get_by_id_customer_service(db: Session, cust_id: uuid.UUID):
    customer = get_customer_by_id(db, cust_id)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

def get_by_email_customer_service(db: Session, email: EmailStr):
    customer = get_customer_by_email(db, email)
    if customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

def create_customer_service(db: Session, customer: CustomerCreate):
    if check_email(customer, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer already exists")

    if check_phone_number(customer, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer already exists"
        )

    try:
        db_customer = create_customer(db, customer)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    return db_customer

def update_customer_service(db: Session, id: uuid.UUID, customer: CustomerBase):
    db_customer = get_customer_by_id(db, id)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    try:
        update_data = customer.model_dump(exclude_unset=True)
        return update_customer(db, db_customer, update_data)

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e)
        )

def delete_customer_service(db: Session, id: uuid.UUID):
    db_customer = get_customer_by_id(db, id)
    if db_customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    try:
        delete_customer(db, db_customer)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e)
        )