from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.loan_sales_agent_BL.schemas.credit_score_schema import CreditScoreResponse, CreditScoreCreate
from src.loan_sales_agent_DL.repository.credit_score_repository import (
get_credit_score,
get_credit_scores,
set_credit_score,
update_credit_score,
delete_credit_score
)
def get_all_credit_score_service(db: Session, skip: int = 0, limit: int = 100):
    scores = get_credit_scores(db, skip, limit)

    result = []
    for credit_score in scores:
        result.append({
            'credit_score_id': credit_score.credit_score_id,
            'credit_score': credit_score.credit_score,
            'last_updated': credit_score.last_updated
        })
    return result

def get_credit_score_by_id_service(db: Session, credit_score_id: int):
    credit_score = get_credit_score(db, credit_score_id)
    if not credit_score:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Credit score not found')
    return credit_score

def create_credit_score_service(db: Session, credit_score_create: CreditScoreCreate):
    try:
        db_credit_score = set_credit_score(db, credit_score_create)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return db_credit_score

def update_credit_score_service(db: Session, credit_id: int, credit_score_create: CreditScoreCreate):
    credit_score = get_credit_score(db, credit_id)
    if not credit_score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Credit score not found'
        )
    try:
        updated_credit_score = update_credit_score(db, credit_id, credit_score_create)
        return updated_credit_score
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

def delete_credit_score_service(db: Session, credit_id: int):
    credit_score = get_credit_score(db, credit_id)
    if not credit_score:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Credit score not found'
        )
    try:
        delete_credit_score(db, credit_id)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )







