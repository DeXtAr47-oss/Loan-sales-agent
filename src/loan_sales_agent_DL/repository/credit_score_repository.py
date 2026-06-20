from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from src.loan_sales_agent_BL.schemas.credit_score_schema import CreditScoreCreate, CreditScoreBase, CreditScoreResponse
from src.loan_sales_agent_DL.models.credit_score_model import CreditScore, RelCreditScoreCustomer

async def get_credit_scores(db: AsyncSession, offset: int=0, limit: int=100):
    stmt = select(CreditScore).where(CreditScore.is_deleted == False).offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_credit_score(db: AsyncSession, credit_score_id: int):
    stmt = (
        select(CreditScore)
        .where(CreditScore.credit_score_id == credit_score_id,
               CreditScore.is_deleted == False)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()



async def set_credit_score(db: AsyncSession, credit_score: CreditScoreCreate):
    new_credit_score = CreditScore(
        credit_score=credit_score.credit_score
    )
    db.add(new_credit_score)
    await db.commit()
    await db.refresh(new_credit_score)

    return new_credit_score


async def update_credit_score(db: AsyncSession, credit_id: int, credit_score: CreditScoreCreate):
    db_credit_score = await get_credit_score(db, credit_id)

    if not db_credit_score:
        return None

    db_credit_score.credit_score = credit_score.credit_score
    db_credit_score.last_updated = datetime.utcnow()

    await db.commit()
    await db.refresh(db_credit_score)
    return db_credit_score


async def delete_credit_score(db: AsyncSession, credit_score: CreditScoreBase):
    credit_score.is_deleted = True
    await db.commit()
    await db.refresh(credit_score)
