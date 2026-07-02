from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from src.loan_sales_agent_shared.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)

base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        yield db