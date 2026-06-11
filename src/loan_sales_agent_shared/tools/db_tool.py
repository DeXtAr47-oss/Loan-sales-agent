from src.loan_sales_agent_shared.config import MCP
from src.loan_sales_agent_shared.connection import SessionLocal
from pydantic import EmailStr

from src.loan_sales_agent_DL.repository.customer_repository import get_customer_by_email

@MCP.tool()
def get_customer_by_email_tool(email: EmailStr):
    db = SessionLocal()
    try:
        customer = get_customer_by_email(db, email)

        if customer is None:
            return {
                "customer_id": None
            }
        return {
            "customer_id": customer.customer_id,
            "name": customer.name,
            "age": customer.age
        }

    finally:
        db.close()


