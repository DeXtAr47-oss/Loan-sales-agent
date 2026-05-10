from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.loan_sales_agent_shared.connection import base


class CreditScore(base):
    __tablename__="creditscore"
    customer_id = Column(Integer, ForeignKey('customer.id'), primary_key=True)
    credit_score = Column(Integer, index=True)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    customer = relationship("Customer", back_populates="credit_score")