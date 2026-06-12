from sqlalchemy.orm import Session
from src.loan_sales_agent_BL.schemas.loan_application_schema import LoanApplicationCreate, LoanApplicationBase
from src.loan_sales_agent_DL.models.loan_application_model import LoanApplication

def get_loan_applications(db: Session, cust_id: int):
    return (
        db.query(LoanApplication)
        .filter(LoanApplication.customer_id == cust_id)
        .all()
    )


def get_loan_application(db: Session, application_id: int):
    return (
        db.query(LoanApplication)
        .filter(LoanApplication.application_id == application_id)
        .first()
    )


def create_loan_application(db: Session, cust_id: int, application: LoanApplicationCreate):
    db_application = LoanApplication(
        customer_id=cust_id,
        loan_amount=application.loan_amount,
        tenure_months=application.tenure_months,
        interest_rate=application.interest_rate,
        monthly_emi=application.monthly_emi,
        status=application.status,
        rejection_reason=application.rejection_reason,
        conversation_id=application.conversation_id,
        conversation_history=application.conversation_history
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


def update_conversation_history(db: Session, customer_id: int, conversation_history: LoanApplicationCreate):
    db_conversation = db.query(LoanApplication).filter(LoanApplication.customer_id == customer_id).first()
    if db_conversation:
        db_conversation.conversaion_history = conversation_history.conversation_history
    db.commit()
    db.refresh(db_conversation)
    return db_conversation


def update_loan_application(db: Session, application_id: int, application: LoanApplicationBase):
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
