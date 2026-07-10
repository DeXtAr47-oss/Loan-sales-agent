from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from typing import List, Optional
import uuid

from src.loan_sales_agent_DL.services.connection import get_db
from src.loan_sales_agent_BL.schemas.customer_schema import (
CustomerCreate,
CustomerResponse
)
from src.loan_sales_agent_BL.services.customer_service import (
get_all_customer_service,
get_by_email_customer_service,
get_by_id_customer_service,
create_customer_service,
update_customer_service,
delete_customer_service,
build_customer_response
)

from src.loan_sales_agent_shared.models.pagination_model import PaginatedResponse

from src.loan_sales_agent_BL.services.authentication_service import get_current_user

router = APIRouter(
    prefix="/customers",
    tags=["Customer API"],
    include_in_schema=False
)

api_router = APIRouter(
    prefix="/api/customers",
    tags=["Customer API"]
)

@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer_controller(
    customer: CustomerCreate,
    db: AsyncSession = Depends(get_db)
):
    new_customer = await create_customer_service(db, customer)
    return new_customer

@api_router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer_controller(
    customer: CustomerCreate,
    db: AsyncSession = Depends(get_db)
):
    new_customer = await create_customer_service(db, customer)
    return new_customer

@api_router.get("/", response_model=PaginatedResponse[CustomerResponse], status_code=status.HTTP_200_OK)
async def get_all_customers(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    search_query: str = Query(None, alias="search_query"),
    is_deleted: bool = Query(None, alias = "is_deleted"),
    db: AsyncSession = Depends(get_db)
):
    return await get_all_customer_service(db, page, per_page, search_query, is_deleted)

@router.get(
    "/me",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK
)
async def get_current_customer(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return build_customer_response(current_user)

@router.get("/{customer_id}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def get_id(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    return await get_by_id_customer_service(db, customer_id)

@api_router.get("/{customer_id}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def get_id(
    customer_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    return await get_by_id_customer_service(db, customer_id)

@router.get("/email/{customer_email}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def get_email(
        customer_email: EmailStr,
        db: AsyncSession = Depends(get_db)
):
    return await get_by_email_customer_service(db, customer_email)

@api_router.get("/email/{customer_email}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
async def get_email(
        customer_email: EmailStr,
        db: AsyncSession = Depends(get_db)
):
    return await get_by_email_customer_service(db, customer_email)

@router.put("/me", status_code=status.HTTP_204_NO_CONTENT)
async def update(
        customer: CustomerCreate,
        db: AsyncSession = Depends(get_db),
        current_user = Depends(get_current_user)
):
    user, _ = current_user
    await update_customer_service(db, user.customer_id, customer)
    return {"message": "customer updated"}

@api_router.put("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(
        customer_id: uuid.UUID,
        customer: CustomerCreate,
        db: AsyncSession = Depends(get_db)
):
    await update_customer_service(db, customer_id, customer)
    return {"message": "customer updated"}


@api_router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(customer_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    await delete_customer_service(db, customer_id)
    return {"message": "customer deleted"}
