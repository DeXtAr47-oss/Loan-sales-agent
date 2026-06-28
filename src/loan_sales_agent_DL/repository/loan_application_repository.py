import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.loan_sales_agent_BL.schemas.loan_application_schema import LoanApplicationCreate, LoanApplicationBase
from src.loan_sales_agent_DL.models.loan_application_model import LoanApplication, RelLoanApplicationCustomer

async def get_loan_applications(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(LoanApplication).where(LoanApplication.is_deleted == False).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_loan_application(db: AsyncSession, application_id: int):
    stmt = (
        select(LoanApplication)
        .where(LoanApplication.application_id == application_id,
               LoanApplication.is_deleted == False)
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_active_loan_application_by_customer_id(db: AsyncSession, customer_id: uuid.UUID):
    stmt = (
        select(LoanApplication)
        .outerjoin(RelLoanApplicationCustomer,
                   LoanApplication.application_id == RelLoanApplicationCustomer.application_id
        )
        .where(RelLoanApplicationCustomer.customer_id == customer_id,
               LoanApplication.status == "active",
               LoanApplication.is_deleted == False
               )
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_loan_application(db: AsyncSession, application: LoanApplicationCreate):
    new_loan_application = LoanApplication(
        conversation_id=application.conversation_id,
        conversation_history=application.conversation_history,
        loan_amount=application.loan_amount,
        tenure_months=application.tenure_months,
        interest_rate=application.interest_rate,
        monthly_emi=application.monthly_emi,
        status=application.status,
        rejection_reason=application.rejection_reason,
        is_deleted=False
    )
    db.add(new_loan_application)
    await db.commit()
    await db.refresh(new_loan_application)
    return new_loan_application


async def update_loan_application(db: AsyncSession, application_id: int, application: LoanApplicationBase):
    db_application = await get_loan_application(db, application_id)
    if not db_application:
        return None
    for field, value in application.model_dump(exclude_unset=True).items():
        setattr(db_application, field, value)
    await db.commit()
    await db.refresh(db_application)
    return db_application


async def delete_loan_application(db: AsyncSession, loan_application: LoanApplicationCreate):
    loan_application.is_deleted = True
    await db.commit()
    await db.refresh(loan_application)

