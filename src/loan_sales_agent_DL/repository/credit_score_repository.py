from sqlalchemy.orm import Session
from src.loan_sales_agent_BL.schemas.credit_score_schema import CreditScoreCreate, CreditScoreBase
from src.loan_sales_agent_DL.models.credit_score_model import CreditScore, RelCreditScoreCustomer
from src.loan_sales_agent_DL.models.customer_model import Customer
from uuid import UUID

def get_credit_scores(db: Session):
    return db.query(CreditScore.credit_score).all()


def get_credit_score(db: Session, customer_id: UUID):
    return (
        db.query(CreditScore)
        .join(
            RelCreditScoreCustomer,
            CreditScore.credit_score_id ==
            RelCreditScoreCustomer.credit_score_id
        )
        .join(
            Customer,
            Customer.customer_id ==
            RelCreditScoreCustomer.customer_id
        )
        .filter(Customer.customer_id == customer_id)
        .all()
    )


def set_credit_score(db: Session, cust_id: UUID, credit_score: CreditScoreCreate):
    new_credit_score = CreditScore(
        credit_score=credit_score.credit_score
    )
    db.add(new_credit_score)
    db.flush()

    rel_credit_score_customer = RelCreditScoreCustomer(
        customer_id=cust_id,
        credit_score_id=new_credit_score.credit_score_id
    )

    db.add(rel_credit_score_customer)
    db.commit()
    db.refresh(new_credit_score)
    db.refresh(rel_credit_score_customer)

    return new_credit_score


def update_credit_score(db: Session, cust_id: int, credit_score: CreditScoreBase):
    db_credit_score = get_credit_score(db, cust_id)
    if not db_credit_score:
        return None

    db_credit_score.credit_score = credit_score.credit_score
    db.commit()
    db.refresh(db_credit_score)
    return db_credit_score


def delete_credit_score(db: Session, cust_id: int):
    db_credit_score = get_credit_score(db, cust_id)
    if not db_credit_score:
        return None
    db.delete(db_credit_score)
    db.commit()
    return db_credit_score
