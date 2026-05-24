from sqlalchemy.exc import SQLAlchemyError
from pydantic import EmailStr
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.loan_sales_agent_BL.schemas.customer_schema import CustomerCreate, CustomerBase
from src.loan_sales_agent_DL.models import customer_model as models
from src.loan_sales_agent_DL.models import credit_score_model as credit_score_model
import uuid

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_all_customer(db: Session):
    return db.query(models.Customer).filter(models.Customer.is_deleted.is_(False)).all()


def get_customer_by_id(db: Session, cust_id: uuid.UUID):
    return (
        db.query(models.Customer).filter(models.Customer.customer_id == cust_id,
                                         models.Customer.is_deleted.is_(False))
        .first()
    )


def get_customer_by_email(db: Session, email_id: EmailStr):
    return (
        db.query(models.Customer).filter(models.Customer.email == email_id,
                                         models.Customer.is_deleted.is_(False))
        .first()
    )


def create_customer(db: Session, customer: CustomerCreate):
    hashed_pw = pwd_context.hash(customer.password)
    db_customer = models.Customer(
        customer_id=uuid.uuid4(),
        name=customer.name,
        password=hashed_pw,
        age=customer.age,
        city=customer.city,
        phone=customer.phone,
        address=customer.address,
        email=customer.email,
        is_deleted=False
    )

    db.add(db_customer)
    db.flush()

    if customer.credit_score is not None:
        db_credit_score = credit_score_model.CreditScore(
            credit_score = customer.credit_score
        )
        db.add(db_credit_score)
        db.flush()

        db_rel_credit_score = credit_score_model.RelCreditScoreCustomer(
            customer_id=db_customer.customer_id,
            credit_score_id=db_credit_score.credit_score_id,
        )

        db.add(db_rel_credit_score)

    db.commit()
    db.refresh(db_customer)

    return db_customer


def update_customer(db: Session, db_customer: CustomerBase, update_data: dict):
    try:
        for field, value in update_data.items():
            if hasattr(db_customer, field):
                setattr(db_customer, field, value)

        db.commit()
        db.refresh(db_customer)
        return db_customer
    except SQLAlchemyError as e:
        db.rollback()
        raise e


def delete_customer(db: Session, db_customer: CustomerBase):
    db_customer.is_deleted = True
    db.commit()
    db.refresh(db_customer)

def check_email(customer: CustomerBase, db: Session):
    existing_email = (
        db.query(models.Customer)
        .filter(models.Customer.email == customer.email,
                models.Customer.is_deleted.is_(False))
        .first()
    )
    if existing_email is not None:
        return True
    else:
        return False

def check_phone_number(customer: CustomerBase, db: Session):
    existing_phone_number = (
        db.query(models.Customer)
        .filter(models.Customer.phone == customer.phone,
                models.Customer.is_deleted.is_(False))
        .first()
    )
    if existing_phone_number is not None:
        return True
    else:
        return False
