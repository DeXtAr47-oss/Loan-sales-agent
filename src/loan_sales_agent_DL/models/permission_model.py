from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum, ForeignKey, UUID
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

    rel_customer_permission = relationship("RelPermissionCustomer", back_populates="permission", cascade="all, delete-orphan")

class RelPermissionCustomer(base):
    __tablename__ = "rel_permission_customer"
    rel_permission_customer_id = Column(Integer, primary_key=True)
    permission_id = Column(Integer, ForeignKey("permission.permission_id", ondelete = "CASCADE"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customer.customer_id", ondelete = "CASCADE"))
    is_deleted = Column(Boolean, default=False)

    customer = relationship("Customer", back_populates="permission_rel")
    permission = relationship("Permission", back_populates="rel_customer_permission")