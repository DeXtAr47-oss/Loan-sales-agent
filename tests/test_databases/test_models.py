import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from databases.models import Customer, CreditScore, LoanApplication, LoanOffer, SalarySlip
from databases.connection import base
from config import TEST_DATABASE_URL

@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE_URL)

@pytest.fixture(scope="function")
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    base.metadata.create_all(bind = connection)
    testing_session_local = sessionmaker(bind=connection)
    session = testing_session_local()
    yield session
    session.close()
    transaction.rollback()
    connection.close()

def test_create_customer(session):
    customer = Customer(
        password = "password",
        name = "Pritam Das",
        age = 25,
        city = "Balurghat",
        phone = "+91 8617025415",
        email = "pdas9691@gmail.com"
        )
    
    session.add(customer)
    session.commit()

    db_customer = session.query(Customer).first()

    assert db_customer.name == "Pritam Das"
    assert db_customer.email == "pdas9691@gmail.com"

def test_same_field_customer(session):
    customer1 = Customer(name = "A", password = "password", email = "Atest@email.com", phone = "+91 1234567890")
    customer1_ = Customer(name = "X", password = "password", email = "Atest@email.com", phone = "+91 1234567890")

    session.add(customer1)
    session.commit()

    session.add(customer1_)
    with pytest.raises(IntegrityError):
        session.commit()

def test_CreditScore_relationship(session):
    customer = Customer(
        name="Pritam Das",
        password="password",
        phone="+91 1234567890",
        email="pdas9691@gmail.com"
    )

    credit_score=CreditScore(
        credit_score=470
    )
    customer.credit_score = credit_score
    session.add(customer)
    session.commit()
    db_customer = session.query(Customer).first()
    assert db_customer.credit_score.credit_score == 470

def test_loan_application_and_salary_slips(session):
    customer = Customer(
        password="hashed_pw",
        name="Loan User",
        phone="7777777777",
        email="loan@test.com"
    )

    application = LoanApplication(
        loan_amount=100000,
        tenure_months=12,
        status="pending"
    )

    slip1 = SalarySlip(
        slip_id="SLIP1",
        monthly_salary=50000,
        file_path="/path/slip1.pdf"
    )

    slip2 = SalarySlip(
        slip_id="SLIP2",
        monthly_salary=52000,
        file_path="/path/slip2.pdf"
    )

    application.salary_slips.extend([slip1, slip2])
    customer.loan_application.append(application)

    session.add(customer)
    session.commit()

    db_app = session.query(LoanApplication).first()

    assert len(db_app.salary_slips) == 2

def test_cascade_delete_customer(session):
    customer = Customer(
        password="hashed_pw",
        name="Delete User",
        phone="6666666666",
        email="delete@test.com"
    )

    application = LoanApplication(
        loan_amount=50000,
        tenure_months=6,
        status="approved"
    )

    slip = SalarySlip(
        slip_id="SLIPX",
        monthly_salary=45000,
        file_path="/path/slipx.pdf"
    )

    application.salary_slips.append(slip)
    customer.loan_application.append(application)

    session.add(customer)
    session.commit()

    session.delete(customer)
    session.commit()

    assert session.query(Customer).count() == 0
    assert session.query(LoanApplication).count() == 0
    assert session.query(SalarySlip).count() == 0