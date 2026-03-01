from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .connection import base

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
    loan_offers = relationship("LonaOffer", back_populates="laonoffer", cascade="all, delete-orphan")
    loan_application = relationship("LoanApplication", back_populates="loanapplication", cascade="all, delete-orphan")
    salary_slips = relationship("SalarySlip", back_populates="salaryslip", cascade="all, delete-orphan")

class CreditScore(base):
    __tablename__="creditscore"
    customer_id = Column(Integer, ForeignKey('customer.id'), primary_key=True)
    credit_score = Column(Integer, index=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="credit_score")

class LoanOffer(base):
    __tablename__="loanoffer"
    offer_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), unique=True, index=True)
    amount_range_min = Column(Numeric(12, 2))
    amount_range_max = Column(Numeric(12, 2))
    interest_rate = Column(Numeric(2, 1))
    tenure_months = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="loan_offers")

class LoanApplicaiton(base):
    __tablename__="loanapplication"
    application_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id', ondelete="CASCADE"), index=True)
    conversation_id = Column(String(255))
    loan_amount = Column(Numeric(12, 2))
    tenure_months = Column(Integer)
    interest_rate = Column(Numeric(2, 1))
    monthly_emi = Column(Integer)
    status = Column(String(100))
    rejection_reason = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="loan_application")

class SalarySlip(base):
    __tablename__="salaryslip"
    slip_id = Column(String(255), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id', ondelete='CASCADE'), index=True)
    application_id = Column(Integer, ForeignKey('loanapplication.application_id', ondelete='CASCADE'))
    monthly_salary = Column(Numeric(12, 2))
    file_path = Column(String(255))
    upload_date = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="salary_slips")
    