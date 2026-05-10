from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.loan_sales_agent_shared.connection import base

class LoanApplication(base):
    __tablename__="loanapplication"
    application_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id', ondelete="CASCADE"), index=True)
    conversation_id = Column(String(255))
    conversaion_history = Column(String(1024))
    loan_amount = Column(Numeric(12, 2))
    tenure_months = Column(Integer)
    interest_rate = Column(Numeric(2, 1))
    monthly_emi = Column(Integer)
    status = Column(String(100))
    rejection_reason = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="loan_application")
    salary_slips = relationship("SalarySlip", back_populates="loanapplication", cascade="all, delete-orphan")