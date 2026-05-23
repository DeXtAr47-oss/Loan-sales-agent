from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, UUID, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.loan_sales_agent_shared.connection import base

class LoanApplication(base):
    __tablename__="loan_application"
    application_id = Column(Integer, primary_key=True)
    conversation_id = Column(String(255))
    conversation_history = Column(String(1024))
    loan_amount = Column(Numeric(12, 2))
    tenure_months = Column(Integer)
    interest_rate = Column(Numeric(2, 1))
    monthly_emi = Column(Integer)
    status = Column(String(100))
    rejection_reason = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean, default=False)

    rel_customer = relationship("RelLoanApplicationCustomer", back_populates="loan_application", cascade="all, delete-orphan")
    rel_salary_slips = relationship("RelSalarySlipLoanApplication", back_populates="loan_application", cascade="all, delete-orphan")

class RelLoanApplicationCustomer(base):
    __tablename__="rel_loan_application_customer"
    rel_loan_application_customer_id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey('loan_application.application_id', ondelete="CASCADE"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customer.customer_id', ondelete="CASCADE"))
    is_deleted = Column(Boolean, default=False)

    customer = relationship("Customer", back_populates="loan_application_rel")
    loan_application = relationship("LoanApplication", back_populates="rel_customer")