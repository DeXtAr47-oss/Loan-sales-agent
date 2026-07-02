from sqlalchemy import Column, Integer,UUID, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.loan_sales_agent_DL.services.connection import base


class CreditScore(base):
    __tablename__="credit_score"
    credit_score_id = Column(Integer, primary_key=True, autoincrement=True)
    credit_score = Column(Integer)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    rel_customer = relationship("RelCreditScoreCustomer", back_populates="credit_score", cascade="all, delete-orphan")

class RelCreditScoreCustomer(base):
    __tablename__="rel_credit_score_customer"
    rel_credit_score_customer_id = Column(Integer, primary_key=True, autoincrement=True)
    credit_score_id = Column(Integer, ForeignKey("credit_score.credit_score_id", ondelete="CASCADE"))
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customer.customer_id", ondelete="CASCADE"))
    is_deleted = Column(Boolean, default=False)

    customer = relationship("Customer", back_populates="credit_score_rel")
    credit_score = relationship("CreditScore", back_populates="rel_customer")