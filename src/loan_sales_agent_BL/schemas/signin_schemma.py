from pydantic import BaseModel, EmailStr
import uuid

class SigninRequest(BaseModel):
    email: EmailStr
    password: str

class UserInfo(BaseModel):
    customer_id: uuid.UUID
    name: str
    email: EmailStr

class SigninResponse(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    user: UserInfo
