from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.loan_sales_agent_BL.schemas.signin_schemma import SigninRequest, SigninResponse, UserInfo
from src.loan_sales_agent_BL.services.authentication_service import authenticate_user
from src.loan_sales_agent_shared.auth import create_access_token

async def authentication_services(db: AsyncSession, login_data: SigninRequest):
    user = await authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail = 'Invalid credentials')

    access_token = create_access_token(
        {
            "sub": user.email,
            "customer_id": str(user.customer_id)
        }
    )

    return SigninResponse(
        access_token=access_token,
        token_type="Bearer",
        user=UserInfo(
            customer_id=user.customer_id,
            name=user.name,
            email=user.email
        )
    )
