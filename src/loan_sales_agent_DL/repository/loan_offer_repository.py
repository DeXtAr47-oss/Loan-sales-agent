from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Select
from src.loan_sales_agent_BL.schemas.loan_offer_schema import LoanOfferRequest
from src.loan_sales_agent_DL.models.loan_offer_model import LoanOffer

async def get_loan_offers(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = Select(LoanOffer).where(LoanOffer.is_deleted == False).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_loan_offer(db: AsyncSession, offer_id: int):
    stmt = (
        Select(LoanOffer)
        .where(LoanOffer.offer_id == offer_id,
               LoanOffer.is_deleted == False)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_loan_offer(db: AsyncSession, loan_offer: LoanOfferRequest):
    new_loan_offer = LoanOffer(
        amount_range_min=loan_offer.amount_range_min,
        amount_range_max=loan_offer.amount_range_max,
        interest_rate=loan_offer.interest_rate,
        tenure_months=loan_offer.tenure_months,
        is_deleted=False
    )
    db.add(new_loan_offer)
    await db.commit()
    await db.refresh(new_loan_offer)

    return new_loan_offer


async def update_loan_offer(db: AsyncSession, offer_id: int, loan_offer: LoanOfferRequest):
    db_loan_offer = await get_loan_offer(db, offer_id)
    if not db_loan_offer:
        return None
    for field, value in loan_offer.model_dump(exclude_unset=True).items():
        setattr(db_loan_offer, field, value)

    await db.commit()
    await db.refresh(db_loan_offer)
    return db_loan_offer


async def delete_loan_offer(db: AsyncSession, loan_offer: LoanOfferRequest):
    loan_offer.is_deleted = True
    await db.commit()
    await db.refresh(loan_offer)