from sqlalchemy.orm import Session
from src.loan_sales_agent_BL.schemas.loan_offer_schema import LoanOfferCreate
import models.loan_offer_model as models

def get_loan_offers(db: Session, cust_id: int):
    return (
        db.query(models.LoanOffer)
        .filter(models.LoanOffer.customer_id == cust_id)
        .all()
    )


def get_loan_offer(db: Session, offer_id: int):
    return (
        db.query(models.LoanOffer)
        .filter(models.LoanOffer.offer_id == offer_id)
        .first()
    )


def create_loan_offer(db: Session, cust_id: int, loan_offer: LoanOfferCreate):
    db_loan_offer = models.LoanOffer(
        customer_id=cust_id,
        amount_range_min=loan_offer.amount_range_min,
        amount_range_max=loan_offer.amount_range_max,
        interest_rate=loan_offer.interest_rate,
        tenure_months=loan_offer.tenure_months,
    )
    db.add(db_loan_offer)
    db.commit()
    db.refresh(db_loan_offer)
    return db_loan_offer


def update_loan_offer(db: Session, offer_id: int, loan_offer: LoanOfferCreate):
    db_loan_offer = get_loan_offer(db, offer_id)
    if not db_loan_offer:
        return None
    for field, value in loan_offer.model_dump(exclude_unset=True).items():
        setattr(db_loan_offer, field, value)
    db.commit()
    db.refresh(db_loan_offer)
    return db_loan_offer


def delete_loan_offer(db: Session, offer_id: int):
    db_loan_offer = get_loan_offer(db, offer_id)
    if not db_loan_offer:
        return None
    db.delete(db_loan_offer)
    db.commit()
    return db_loan_offer