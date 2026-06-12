from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List

from src.loan_sales_agent_shared.connection import get_db
from src.loan_sales_agent_BL.schemas.credit_score_schema import (
CreditScoreCreate,
CreditScoreResponse
)
from src.loan_sales_agent_BL.services.credit_score_service import (
get_all_credit_score_service,
get_credit_score_by_id_service,
create_credit_score_service,
update_credit_score_service,
delete_credit_score_service
)

credit_score_api_router = APIRouter(
    prefix="/api/credit-score",
    tags=["Credit Score API"]
)

@credit_score_api_router.get("/", response_model=List[CreditScoreResponse], status_code=status.HTTP_200_OK)
def get_credit_scores(db: Session = Depends(get_db)):
    return get_all_credit_score_service(db)

@credit_score_api_router.get("/{credit_score_id}", response_model=CreditScoreResponse, status_code=status.HTTP_200_OK)
def get_credit_score_by_id(credit_score_id: int, db: Session = Depends(get_db)):
    return get_credit_score_by_id_service(db, credit_score_id)

@credit_score_api_router.post("/", response_model=CreditScoreResponse, status_code=status.HTTP_201_CREATED)
def create_credit_score(credit_score: CreditScoreCreate, db: Session = Depends(get_db)):
    new_credit_score = create_credit_score_service(db, credit_score)
    return new_credit_score

@credit_score_api_router.put("/{credit_score_id}", response_model=CreditScoreResponse, status_code=status.HTTP_202_ACCEPTED)
def update_credit_score(
    credit_score_id: int,
    credit_score: CreditScoreCreate,
    db: Session = Depends(get_db),
):
    updated_credit_score = update_credit_score_service(db, credit_score_id, credit_score)
    return updated_credit_score

@credit_score_api_router.delete("/{credit_score_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_credit_score(credit_score_id: int, db: Session = Depends(get_db)):
    delete_credit_score_service(db, credit_score_id)
    return {"message": "Credit score deleted"}

