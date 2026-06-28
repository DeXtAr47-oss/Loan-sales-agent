from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.loan_sales_agent_BL.schemas.loan_offer_schema import LoanOfferRequest, LoanOfferResponse
from src.loan_sales_agent_DL.repository.loan_offer_repository import (
get_loan_offers,
get_loan_offer,
create_loan_offer,
update_loan_offer,
delete_loan_offer,
)

async def get_all_loan_offers_service(db: AsyncSession, skip: int = 0, limit: int = 100):
    scores = await get_loan_offers(db, skip, limit)

    result = []
    for score in scores:
        result.append({
            "offer_id": score.offer_id,
            "amount_range_min": score.amount_range_min,
            "amount_range_max": score.amount_range_max,
            "interest_rate": score.interest_rate,
            "tenure_months": score.tenure_months,
            "created_at": score.created_at
        })
    return result

async def get_loan_offer_by_id_service(db: AsyncSession, loan_id: int):
    loan_offer = await get_loan_offer(db, loan_id)
    if not loan_offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Loan Offer not found')
    return loan_offer

async def create_loan_offer_service(db: AsyncSession, loan_offer_request: LoanOfferRequest):
    try:
        loan_offer = await create_loan_offer(db, loan_offer_request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return loan_offer

async def update_loan_offer_service(db: AsyncSession, loan_offer_id: int, loan_offer_request: LoanOfferRequest):
    loan_offer = await get_loan_offer(db, loan_offer_id)
    if not loan_offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Loan Offer not found')

    try:
        updated_loan_offer = await update_loan_offer(db, loan_offer_id, loan_offer_request)
        return updated_loan_offer
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

async def delete_loan_offer_service(db: AsyncSession, loan_offer_id: int):
    loan_offer = await get_loan_offer(db, loan_offer_id)
    if not loan_offer:
        raise HTTPException(status_code=404, detail='Loan Offer not found')
    try:
        await delete_loan_offer(db, loan_offer)
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )