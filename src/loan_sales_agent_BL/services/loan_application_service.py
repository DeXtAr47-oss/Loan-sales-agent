import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.loan_sales_agent_BL.schemas.loan_application_schema import LoanApplicationCreate, LoanApplicationResponse, \
    LoanApplicationBase
from src.loan_sales_agent_DL.repository.loan_application_repository import (
get_loan_applications,
get_loan_application,
create_loan_application,
update_loan_application,
delete_loan_application
)

async def get_all_loan_applications(db: AsyncSession, skip: int = 0, limit: int = 100):
    applications = await get_loan_applications(db, skip=skip, limit=limit)

    result = []
    for application in applications:
        result.append({
            "application_id": application.application_id,
            "conversation_id": application.conversation_id,
            "conversation_history": application.conversation_history,
            "loan_amount": application.loan_amount,
            "tenure_months": application.tenure_months,
            "interest_rate": application.interest_rate,
            "monthly_emi": application.montthly_emi,
            "status": application.status,
            "rejection_reason": application.rejection_reason,
            "created_at": application.created_at,
            "approved_at": application.approved_at
        })
    return result

async def get_loan_application_by_id(db: AsyncSession, loan_id: int):
    loan_application = await get_loan_application(db, loan_id)
    if not loan_application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan application not found")
    return loan_application

async def create_loan_application_service(db: AsyncSession, loan_application_request: LoanApplicationCreate):
    try:
        loan_application = await create_loan_application(db, loan_application_request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return loan_application

async def update_loan_application_service(db: AsyncSession, loan_application_id: int, loan_application: LoanApplicationBase):
    loan_application = await get_loan_application_by_id(db, loan_application_id)
    if not loan_application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan application not found")

    try:
        updated_loan_application = await update_loan_application(db, loan_application)
        return updated_loan_application
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

async def delete_loan_application_service(db: AsyncSession, loan_application_id: int):
    loan_application = await get_loan_application_by_id(db, loan_application_id)
    if not loan_application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan application not found")
    try:
        await delete_loan_application(db, loan_application)
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



