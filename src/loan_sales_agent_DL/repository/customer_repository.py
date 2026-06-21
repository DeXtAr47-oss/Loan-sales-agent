from sqlalchemy.exc import SQLAlchemyError
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.loan_sales_agent_BL.schemas.customer_schema import CustomerCreate, CustomerBase
from src.loan_sales_agent_DL.models import customer_model as models
from src.loan_sales_agent_DL.models.credit_score_model import RelCreditScoreCustomer, CreditScore
from src.loan_sales_agent_DL.repository.credit_score_repository import set_credit_score, update_credit_score
from src.loan_sales_agent_BL.schemas.credit_score_schema import CreditScoreCreate
from src.loan_sales_agent_shared.config import pwd_context
import uuid

async def get_all_customer(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = (
        select(models.Customer, CreditScore)
        .outerjoin(
            RelCreditScoreCustomer,
            models.Customer.customer_id == RelCreditScoreCustomer.customer_id
        )
        .outerjoin(
            CreditScore,
            RelCreditScoreCustomer.credit_score_id == CreditScore.credit_score_id
        )
        .where(
            models.Customer.is_deleted.is_(False)
        )
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)

    customers_map = {}
    for customer, credit_score in result.all():
        customers_map.setdefault(
            customer.customer_id,
            (customer, credit_score)
        )

    return list(customers_map.values())

async def get_customer_by_id(
    db: AsyncSession,
    cust_id: uuid.UUID
):
    stmt = (
        select(models.Customer, CreditScore)
        .outerjoin(
            RelCreditScoreCustomer,
            models.Customer.customer_id == RelCreditScoreCustomer.customer_id
        )
        .outerjoin(
            CreditScore,
            RelCreditScoreCustomer.credit_score_id == CreditScore.credit_score_id
        )
        .where(
            models.Customer.customer_id == cust_id,
            models.Customer.is_deleted.is_(False)
        )
    )
    result = await db.execute(stmt)
    return result.first()

async def get_customer_by_email(db: AsyncSession, email_id: EmailStr):
    stmt = (
        select(models.Customer)
        .options(
            joinedload(models.Customer.credit_score_rel)
            .joinedload(RelCreditScoreCustomer.credit_score)
        )
        .where(
            models.Customer.email == email_id,
            models.Customer.is_deleted.is_(False)
        )
    )

    result = await db.execute(stmt)

    return result.unique().scalar_one_or_none()


async def create_customer(db: AsyncSession, customer: CustomerCreate):
    hashed_pw = pwd_context.hash(customer.password)
    db_customer = models.Customer(
        customer_id=uuid.uuid4(),
        name=customer.name,
        password=hashed_pw,
        age=customer.age,
        city=customer.city,
        phone=customer.phone,
        address=customer.address,
        email=customer.email,
        is_deleted=False
    )

    db.add(db_customer)
    await db.flush()

    if customer.credit_score is not None:
        new_credit_score = await set_credit_score(db, customer.credit_score)

        rel_credit_score_customer = RelCreditScoreCustomer(
            customer_id=db_customer.customer_id,
            credit_score_id=new_credit_score.credit_score_id
        )
        db.add(rel_credit_score_customer)

    await db.commit()
    await db.refresh(db_customer)

    return db_customer


async def update_customer(
    db: AsyncSession,
    customer_id: uuid.UUID,
    db_customer,
    update_data: dict,
    existing_credit_score
):
    try:
        credit_score_data = update_data.pop("credit_score", None)

        if credit_score_data is not None:
            score_value = (
                credit_score_data.get("credit_score")
                if isinstance(credit_score_data, dict)
                else credit_score_data
            )

            if score_value is not None:

                if existing_credit_score:
                    credit_score_update = CreditScoreCreate(
                        credit_score=score_value
                    )

                    await update_credit_score(
                        db,
                        credit_id=existing_credit_score.credit_score_id,
                        credit_score=credit_score_update
                    )

                else:
                    credit_score_create = CreditScoreCreate(
                        credit_score=score_value
                    )

                    new_credit_score = await set_credit_score(
                        db,
                        credit_score_create
                    )

                    db.add(
                        RelCreditScoreCustomer(
                            customer_id=customer_id,
                            credit_score_id=new_credit_score.credit_score_id
                        )
                    )

        # Update customer fields
        for field, value in update_data.items():
            setattr(db_customer, field, value)

        await db.commit()
        await db.refresh(db_customer)

        return db_customer

    except SQLAlchemyError:
        await db.rollback()
        raise

async def delete_customer(db: AsyncSession, db_customer: CustomerBase):
    db_customer.is_deleted = True
    await db.commit()
    await db.refresh(db_customer)

async def check_email(customer: CustomerBase, db: AsyncSession):
    stmt = select(models.Customer).where(models.Customer.email == customer.email, models.Customer.is_deleted.is_(False))
    result = await db.execute(stmt)
    existing_email = result.scalar_one_or_none()
    if existing_email is not None:
        return True
    else:
        return False

async def check_phone_number(customer: CustomerBase, db: AsyncSession):
    stmt = select(models.Customer).where(models.Customer.phone == customer.phone, models.Customer.is_deleted.is_(False))
    result = await db.execute(stmt)
    existing_phone_number = result.scalar_one_or_none()
    if existing_phone_number is not None:
        return True
    else:
        return False
