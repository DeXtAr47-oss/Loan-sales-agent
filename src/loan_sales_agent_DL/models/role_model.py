from sqlalchemy import String, Boolean, Integer, DateTime, Enum, Column
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from src.loan_sales_agent_DL.enums.role_enums import RoleEnums
from src.loan_sales_agent_DL.services.connection import base

class Role(base):
    __tablename__ = "role"
    