from sqlalchemy.exc import SQLAlchemyError
from pydantic import EmailStr
from sqlalchemy.orm import Session, joinedload
from passlib.context import CryptContext

from src.loan_sales_agent_BL.schemas.customer_schema import CustomerCreate, CustomerBase
from src.loan_sales_agent_DL.models import customer_model as models
from src.loan_sales_agent_DL.models.credit_score_model import RelCreditScoreCustomer, CreditScore
from src.loan_sales_agent_DL.repository.credit_score_repository import set_credit_score
import uuid

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_all_customer(db: Session, skip: int = 0, limit: int = 100):
    results = db.query(
        models.Customer,
        CreditScore
    ).outerjoin(
        RelCreditScoreCustomer,
        models.Customer.customer_id == RelCreditScoreCustomer.customer_id
    ).outerjoin(
        CreditScore,
        RelCreditScoreCustomer.credit_score_id == CreditScore.credit_score_id
    ).filter(
        models.Customer.is_deleted.is_(False)
    ).offset(skip).limit(limit).all()


    customers_map = {}
    for customer, credit_score in results:
        if customer.customer_id not in customers_map:
            customers_map[customer.customer_id] = (customer, credit_score)

    return list(customers_map.values())


def get_customer_by_id(db: Session, cust_id: uuid.UUID):
    result = db.query(
        models.Customer,
        CreditScore
    ).outerjoin(
        RelCreditScoreCustomer,
        models.Customer.customer_id == RelCreditScoreCustomer.customer_id
    ).outerjoin(
        CreditScore,
        RelCreditScoreCustomer.credit_score_id == CreditScore.credit_score_id
    ).filter(
        models.Customer.customer_id == cust_id,
        models.Customer.is_deleted.is_(False)
    ).first()

    if result is None:
        return None, None

    return result[0], result[1]

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
        new_credit_score = set_credit_score(db, customer.credit_score)

        rel_credit_score_customer = RelCreditScoreCustomer(
            customer_id=db_customer.customer_id,
            credit_score_id=new_credit_score.credit_score_id
        )
        db.add(rel_credit_score_customer)

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
