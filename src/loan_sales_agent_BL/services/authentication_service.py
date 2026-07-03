from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from pydantic import EmailStr

from src.loan_sales_agent_shared.auth import verify_token
from src.loan_sales_agent_shared.config import pwd_context
from src.loan_sales_agent_BL.services.customer_service import get_customer_by_email
from src.loan_sales_agent_DL.services.connection import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/signin")

security = HTTPBearer(auto_error=False)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    return await get_current_user_helper(token, db)


async def get_current_user_api(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
):
    if credentials is None:
        return None

    token = credentials.credentials
    return await get_current_user_helper(token, db)

async def get_current_user_helper(token, db: AsyncSession):
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    email = payload.get("sub")
    user = await get_customer_by_email(db, email)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect email or password"
        )
    return user


async def authenticate_user(db: AsyncSession, email: EmailStr, password: str):
    result = await get_customer_by_email(db, email)

    if not result:
        return None

    user= result

    if not pwd_context.verify(password, user.password):
        return None

    return user



