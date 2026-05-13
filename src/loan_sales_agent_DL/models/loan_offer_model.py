from sqlalchemy import Column, Integer, Boolean, Numeric, DateTime, ForeignKey, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.loan_sales_agent_shared.connection import base

class LoanOffer(base):
    __tablename__="loan_offer"
    offer_id = Column(Integer, primary_key=True)
    amount_range_min = Column(Numeric(12, 2))
    amount_range_max = Column(Numeric(12, 2))
    interest_rate = Column(Numeric(2, 1))
    tenure_months = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    rel_customer = relationship("RelLoanOfferCustomer", back_populates="loan_offers")

class RelLoanOfferCustomer(base):
    __tablename__="rel_loan_offer_customer"
    rel_offer_customer_id = Column(Integer, autoincrement=True, primary_key=True)
    offer_id = Column(Integer, ForeignKey('loan_offer.offer_id'))
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customer.customer_id'))
    is_deleted = Column(Boolean, default=False)

    customer = relationship("Customer", back_populates="loan_offers_rel")
    loan_offers = relationship("LoanOffer", back_populates="rel_customer")
