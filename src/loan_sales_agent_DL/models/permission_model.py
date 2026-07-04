from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from enum import Enum

from src.loan_sales_agent_DL.services.connection import base

class PermissionEnums(str, Enum):
    VIEW = "VIEW"
    EDIT = "EDIT"
    CREATE = "CREATE"

class Permission(base):
    __tablename__ = "permission"
    permission_id = Column(Integer, primary_key=True)
