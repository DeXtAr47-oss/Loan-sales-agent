from src.loan_sales_agent_shared.connection import base, engine
from src.loan_sales_agent_DL.models.credit_score_model import CreditScore, RelCreditScoreCustomer
from src.loan_sales_agent_DL.models.customer_model import Customer
from src.loan_sales_agent_DL.models.loan_application_model import LoanApplication, RelLoanApplicationCustomer
from src.loan_sales_agent_DL.models.loan_offer_model import LoanOffer, RelLoanOfferCustomer
from src.loan_sales_agent_DL.models.salary_slip_model import SalarySlip, RelSalarySlipCustomer, RelSalarySlipLoanApplication


base.metadata.create_all(bind=engine)
print('database created')