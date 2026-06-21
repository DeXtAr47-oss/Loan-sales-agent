from datetime import datetime, timedelta
from jose import jwt, JWTError

from src.loan_sales_agent_shared.config import AUTH_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        AUTH_KEY,
        algorithm=ALGORITHM
    )

def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            AUTH_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None 
