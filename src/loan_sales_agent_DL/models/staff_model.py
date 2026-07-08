from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, UUID, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from src.loan_sales_agent_DL.services.connection import base

class Staff(base):
    __tablename__ = "staff"
    staff_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    staff_name = Column(String(225), nullable=False)
    staff_age = Column(Integer)
    staff_email = Column(String(225), nullable=False)
    staff_phone = Column(String(15), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_admin = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)

    permission_rel = relationship("RelPermissionStaff", back_populates="staff", cascade="all, delete-orphan")