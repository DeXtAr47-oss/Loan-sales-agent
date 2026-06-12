from sqlalchemy.orm import Session
from datetime import datetime

from src.loan_sales_agent_BL.schemas.credit_score_schema import CreditScoreCreate, CreditScoreBase, CreditScoreResponse
from src.loan_sales_agent_DL.models.credit_score_model import CreditScore, RelCreditScoreCustomer

def get_credit_scores(db: Session, offset: int=0, limit: int=100):
    scores = db.query(CreditScore).offset(offset).limit(limit).all()
    return [CreditScoreResponse.model_validate(credit_score) for credit_score in scores]


def get_credit_score(db: Session, credit_score_id: int):
    result = (db.query(CreditScore)
              .filter(CreditScore.credit_score_id == credit_score_id,
                      CreditScore.is_deleted.is_(False))
              .first())
    return result



def set_credit_score(db: Session, credit_score: CreditScoreCreate):
    new_credit_score = CreditScore(
        credit_score=credit_score.credit_score
    )
    db.add(new_credit_score)
    db.commit()
    db.refresh(new_credit_score)

    return new_credit_score


def update_credit_score(db: Session, credit_id: int, credit_score: CreditScoreCreate):
    db_credit_score = get_credit_score(db, credit_id)

    if not db_credit_score:
        return None

    db_credit_score.credit_score = credit_score.credit_score
    db_credit_score.last_updated = datetime.utcnow()

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
