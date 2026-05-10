from sqlalchemy.orm import Session
from src.loan_sales_agent_BL.schemas.credit_score_schema import CreditScoreCreate, CreditScoreBase
import models.credit_score_model as models


def get_credit_scores(db: Session):
    return db.query(models.Salary_slip).all()


def get_credit_score(db: Session, cust_id: int):
    return (
        db.query(models.CreditScore)
        .filter(models.CreditScore.customer_id == cust_id)
        .first()
    )


def set_credit_score(db: Session, cust_id: int, credit_score: CreditScoreCreate):
    db_credit_score = models.CreditScore(
        customer_id=cust_id,
        credit_score=credit_score.credit_score
    )
    db.add(db_credit_score)
    db.commit()
    db.refresh(db_credit_score)
    return db_credit_score


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
