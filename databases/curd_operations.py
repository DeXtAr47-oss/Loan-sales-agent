from sqlalchemy.orm import Session
import models, schemas

def get_customers(db: Session):
    return db.query(models.Customer).all()

def get_customer(db: Session, cust_id: int):
    return (
        db.query(models.Customer).filter(models.Customer.id == cust_id).first()
        )

def create_customer(db: Session, customer: schemas.CustomerCreate):
    db_customer = models.Customer(
        name = customer.name,
        password = customer.password,
        age = customer.age,
        city = customer.city,
        phone = customer.phone,
        address = customer.address,
        email = customer.email,
        current_loan_amount = customer.current_loan_amount,
        pre_approved_limit = customer.pre_approved_limit
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, id: int, customer: schemas.CustomerBase):
    db_customer = get_customer(db, id)
    if not db_customer:
        return None
    
    for field, value in customer.model_dump(exclude_unset=True).items():
        setattr(db_customer, field, value)

    db.commit()
    db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, id: int):
    db_employee = get_customer(db, id)
    if not db_employee:
        return None
    
    db.delete(db_employee)
    db.commit()
    return db_employee


def get_credit_scores(db: Session):
    return db.query(models.SalarySlip).all()

def get_credit_score(db: Session, cust_id: int):
    return (
        db.query(models.CreditScore)
        .filter(models.CreditScore.customer_id == cust_id)
        .first()
    )

def set_credit_score(db: Session, cust_id: int, credit_score: schemas.CreditScoreCreate):
    db_credit_score = models.CreditScore(
        customer_id = cust_id,
        credit_score = credit_score.credit_score
    )
    db.add(db_credit_score)
    db.commit()
    db.refresh(db_credit_score)
    return db_credit_score

def update_credit_score(db: Session, cust_id: int, credit_score: schemas.CreditScoreBase):
    db_credit_score = get_credit_score(db, cust_id)
    if not db_credit_score:
        return None
    
    db_credit_score.credit_score = credit_score.credit_score
    db.commit()
    db.refresh(db_credit_score)
    return db_credit_score

def delete_credit_score(db: Session, cust_id: int):
    db_credit_score = get_credit_score(db, cust_id)
    if not db_credit_score:
        return None
    db.delete(db_credit_score)
    db.commit()
    return db_credit_score



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
 
 
def create_loan_offer(db: Session, cust_id: int, loan_offer: schemas.LoanOfferCreate):
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
 
 
def update_loan_offer(db: Session, offer_id: int, loan_offer: schemas.LoanOfferCreate):
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
 


def get_loan_applications(db: Session, cust_id: int):
    return (
        db.query(models.LoanApplication)
        .filter(models.LoanApplication.customer_id == cust_id)
        .all()
    )
 
 
def get_loan_application(db: Session, application_id: int):
    return (
        db.query(models.LoanApplication)
        .filter(models.LoanApplication.application_id == application_id)
        .first()
    )
 
 
def create_loan_application(db: Session, cust_id: int, application: schemas.LoanApplicationCreate):
    db_application = models.LoanApplication(
        customer_id=cust_id,
        loan_amount=application.loan_amount,
        tenure_months=application.tenure_months,
        interest_rate=application.interest_rate,
        monthly_emi=application.monthly_emi,
        status=application.status,
        rejection_reason=application.rejection_reason,
        conversation_id=application.conversation_id,
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application
 
 
def update_loan_application(db: Session, application_id: int, application: schemas.LoanApplicationBase):
    db_application = get_loan_application(db, application_id)
    if not db_application:
        return None
    for field, value in application.model_dump(exclude_unset=True).items():
        setattr(db_application, field, value)
    db.commit()
    db.refresh(db_application)
    return db_application
 
 
def delete_loan_application(db: Session, application_id: int):
    db_application = get_loan_application(db, application_id)
    if not db_application:
        return None
    db.delete(db_application)
    db.commit()
    return db_application



def get_salary_slips(db: Session):
    return db.query(models.SalarySlip).all()

def get_salary_slip(db: Session, cust_id: int):
    return (
        db.query(models.SalarySlip)
        .filter(models.SalarySlip.customer_id == cust_id)
        .first()
    )

def set_salary_slip(db: Session, cust_id: int, salary_slip: schemas.SalarySlipCreate):
    db_salary_slip = models.SalarySlip(
        customer_id=cust_id,
        application_id=salary_slip.application_id,
        monthly_salary=salary_slip.monthly_salary,
        file_path=salary_slip.file_path
    )
    db.add(db_salary_slip)
    db.commit()
    db.refresh(db_salary_slip)
    return db_salary_slip

def update_salary_slip(db: Session, cust_id: int, salary_slip: schemas.SalarySlipBase):
    db_salary_slip = get_salary_slip(db, cust_id)
    if not db_salary_slip:
        return None
    
    for field, values in salary_slip.model_dump(exclude_unset=True).first():
        setattr(db_salary_slip, field, values)

    db.commit()
    db.refresh(db_salary_slip)
    return db_salary_slip

def delete_salary_slip(db: Session, cust_id: int):
    db_salary_slip = get_salary_slip(db, cust_id)
    if not db_salary_slip:
        return None
    
    db.delete(db_salary_slip)
    db.commit()
    return db_salary_slip
