from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.loan_sales_agent_shared.connection import base

class Customer(base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
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

    credit_score = relationship("CreditScore", back_populates="customer", uselist=False, cascade="all, delete-orphan")
    loan_offers = relationship("LoanOffer", back_populates="customer", cascade="all, delete-orphan")
    loan_application = relationship("LoanApplication", back_populates="customer", cascade="all, delete-orphan")
    salary_slips = relationship("SalarySlip", back_populates="customer", cascade="all, delete-orphan")
