from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, UUID, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.loan_sales_agent_shared.connection import base

class SalarySlip(base):
    __tablename__="salary_slip"
    slip_id = Column(String(255), primary_key=True)
    monthly_salary = Column(Numeric(12, 2))
    file_path = Column(String(255))
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    is_deleted = Column(Boolean, default=False)

    rel_customer = relationship("RelSalarySlipCustomer", back_populates="salary_slips", cascade="all, delete-orphan")
    rel_loan_applications = relationship("RelSalarySlipLoanApplication", back_populates="salary_slip", cascade="all, delete-orphan")

class RelSalarySlipCustomer(base):
    __tablename__ = "rel_salary_slip_customer"
    rel_salary_slip_customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customer.customer_id", ondelete='CASCADE'))
    slip_id = Column(String(255), ForeignKey('salary_slip.slip_id', ondelete='CASCADE'))
    is_deleted = Column(Boolean, default=False)

    customer = relationship("Customer", back_populates="salary_slips_rel")
    salary_slips = relationship("SalarySlip", back_populates="rel_customer")

class RelSalarySlipLoanApplication(base):
    __tablename__ = "rel_salary_slip_loan_application"
    rel_salary_slip_loan_application_id = Column(Integer, primary_key=True, autoincrement=True)
    application_id = Column(Integer, ForeignKey('loan_application.application_id', ondelete='CASCADE'))
    slip_id = Column(String(255), ForeignKey('salary_slip.slip_id', ondelete='CASCADE'))
    is_deleted = Column(Boolean, default=False)

    loan_application = relationship("LoanApplication", back_populates="rel_salary_slips")
    salary_slip = relationship("SalarySlip", back_populates="rel_loan_applications")