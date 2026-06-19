from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.loan_sales_agent_shared.connection import get_db
from src.loan_sales_agent_BL.schemas.signin_schemma import SigninRequest, SigninResponse
from src.loan_sales_agent_BL.services.signin_service import authentication_services

signin_router = APIRouter(
    prefix="/signin",
    tags=["Signin"],
    include_in_schema=False
)

api_signin_router = APIRouter(
    prefix="/api/signin",
    tags=["Signin"],
)

@api_signin_router.post("/", response_model=SigninResponse, status_code=status.HTTP_201_CREATED)
async def signin(login_data: SigninRequest, db: AsyncSession = Depends(get_db)):
    return await authentication_services(db, login_data)

@signin_router.post("/", response_model=SigninResponse, status_code=status.HTTP_201_CREATED)
async def signin(login_data: SigninRequest, db: AsyncSession = Depends(get_db)):
    return await authentication_services(db, login_data)