from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from typing import List
import uuid

from src.loan_sales_agent_shared.connection import get_db
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
delete_customer_service
)

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

@api_router.get("/", response_model=List[CustomerResponse], status_code=status.HTTP_200_OK)
async def get_all_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    return await get_all_customer_service(db, skip, limit)

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

@router.put("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update(
        customer_id: uuid.UUID,
        customer: CustomerCreate,
        db: AsyncSession = Depends(get_db)
):
    await update_customer_service(db, customer_id, customer)
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
