from sqlalchemy.orm import Session
from src.loan_sales_agent_BL.schemas.customer_schema import CustomerCreate, CustomerBase
import models.customer_model as models


def get_customers(db: Session):
    return db.query(models.Customer).all()


def get_customer(db: Session, cust_id: int):
    return (
        db.query(models.Customer).filter(models.Customer.customer_id == cust_id).first()
    )


def get_customer_by_email(db: Session, email_id: str):
    return (
        db.query(models.Customer).filter(models.Customer.email == email_id).first()
    )


def create_customer(db: Session, customer: CustomerCreate):
    db_customer = models.Customer(
        name=customer.name,
        password=customer.password,
        age=customer.age,
        city=customer.city,
        phone=customer.phone,
        address=customer.address,
        email=customer.email,
        current_loan_amount=customer.current_loan_amount,
        pre_approved_limit=customer.pre_approved_limit
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def update_customer(db: Session, id: int, customer: CustomerBase):
    db_customer = get_customer(db, id)
    if not db_customer:
        return None

    for field, value in customer.model_dump(exclude_unset=True).items():
        setattr(db_customer, field, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer


def delete_customer(db: Session, id: int):
    db_employee = get_customer(db, id)
    if not db_employee:
        return None

    db.delete(db_employee)
    db.commit()
    return db_employee