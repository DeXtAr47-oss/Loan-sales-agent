from fastapi import FastAPI
from src.loan_sales_agent_API.Customer_controller import router as customer_router
from src.loan_sales_agent_DL import *
app = FastAPI()

app.get("/")
def home():
    return {"message": "Loan sales agent home page"}
app.include_router(customer_router)