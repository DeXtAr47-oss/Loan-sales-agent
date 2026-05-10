from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.loan_sales_agent_shared.connection import base

class SalarySlip(base):
    __tablename__="salaryslip"
    slip_id = Column(String(255), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id', ondelete='CASCADE'), index=True)
    application_id = Column(Integer, ForeignKey('loanapplication.application_id', ondelete='CASCADE'))
    monthly_salary = Column(Numeric(12, 2))
    file_path = Column(String(255))
    upload_date = Column(DateTime(timezone=True), server_default=func.now())

    customer = relationship("Customer", back_populates="salary_slips")
    loanapplication = relationship("LoanApplication", back_populates="salary_slips")