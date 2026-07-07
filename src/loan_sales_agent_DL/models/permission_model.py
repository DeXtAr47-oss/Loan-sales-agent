from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.loan_sales_agent_DL.services.connection import base
from src.loan_sales_agent_DL.enums.permission_enums import PermissionEnums


class Permission(base):
    __tablename__ = "permission"
    permission_id = Column(Integer, primary_key=True)
    permission_key = Column(Enum(PermissionEnums, name="permission_enum"), nullable = False, default=PermissionEnums.VIEW, index=True)
    permission_name = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean, default=False)

