from sqlalchemy import Column, Integer, String, Numeric, DateTime, Boolean, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from src.loan_sales_agent_shared.connection import base

class Customer(base):
    __tablename__ = "customer"
    customer_id = Column(UUID, primary_key=True, default=uuid.uuid4)
    password = Column(String(225), nullable=False)
    name = Column(String(100), index=True)
    age = Column(Integer, index=True)
    city = Column(String(100), index=True)
    phone = Column(String(15), nullable=False, unique=True ,index=True)
    address = Column(String(500))
    email = Column(String(255), nullable=False, unique=True, index=True)
    current_loan_amount = Column(Numeric(12, 2))
    pre_approved_limit = Column(Numeric(12, 2))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    credit_score_rel = relationship("RelCreditScoreCustomer", back_populates="customer", uselist=False, cascade="all, delete-orphan")
    loan_offers_rel = relationship("LoanOffer", back_populates="customer", uselist=False, cascade="all, delete-orphan")
    loan_application_rel = relationship("RelLoanApplicationCustomer", back_populates="customer", uselist=False, cascade="all, delete-orphan")
    salary_slips_rel = relationship("RelSalarySlipCustomer", back_populates="customer", uselist=False, cascade="all, delete-orphan")
