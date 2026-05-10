from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.loan_sales_agent_shared.connection import base

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