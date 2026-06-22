from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.loan_sales_agent_BL.schemas.loan_offer_schema import LoanOfferRequest, LoanOfferResponse
from src.loan_sales_agent_BL.services.loan_offer_service import (
get_all_loan_offers_service,
get_loan_offer_by_id_service,
create_loan_offer_service,
update_loan_offer_service,
delete_loan_offer_service
)
from src.loan_sales_agent_shared.connection import get_db
loan_offer_router_api = APIRouter(
    prefix="/api/loan_offer",
    tags=["Loan offer API"],
)

@loan_offer_router_api.get("/", response_model=List[LoanOfferResponse], status_code=status.HTTP_200_OK)
async def get_all_loan_offers(db: AsyncSession = Depends(get_db),
                              skip: int = Query(0, ge=0),
                              limit: int = Query(100, ge=1, le=1000)
                              ):
    return await get_all_loan_offers_service(db, skip, limit)

@loan_offer_router_api.get("/{loan_offer_id}", response_model=LoanOfferResponse, status_code=status.HTTP_200_OK)
async def get_loan_offer_by_id(loan_offer_id: int, db: AsyncSession = Depends(get_db)):
    return await get_loan_offer_by_id_service(db, loan_offer_id)

@loan_offer_router_api.post("/", response_model=LoanOfferResponse, status_code=status.HTTP_201_CREATED)
async def create_loan_offer(loan_offer: LoanOfferRequest, db: AsyncSession = Depends(get_db)):
    return await create_loan_offer_service(db, loan_offer)

@loan_offer_router_api.put("/{loan_offer_id}", response_model=LoanOfferResponse, status_code=status.HTTP_200_OK)
async def update_loan_offer(loan_offer_id: int, loan_offer: LoanOfferRequest, db: AsyncSession = Depends(get_db)):
    return await update_loan_offer_service(db, loan_offer_id, loan_offer)

@loan_offer_router_api.delete("/{loan_offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_loan_offer( loan_offer_id: int, db: AsyncSession = Depends(get_db)):
    return await delete_loan_offer_service(db, loan_offer_id)
