from sqlalchemy.orm import Session
from src.loan_sales_agent_BL.schemas.salary_slip_schema import SalarySlipCreate, SalarySlipBase
import models.salary_slip_model as models


def get_salary_slips(db: Session):
    return db.query(models.SalarySlip).all()


def get_salary_slip(db: Session, cust_id: int):
    return (
        db.query(models.SalarySlip)
        .filter(models.SalarySlip.customer_id == cust_id)
        .first()
    )


def set_salary_slip(db: Session, cust_id: int, salary_slip: SalarySlipCreate):
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


def update_salary_slip(db: Session, cust_id: int, salary_slip: SalarySlipBase):
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
