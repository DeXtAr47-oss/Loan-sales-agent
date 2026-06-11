import uuid
import datetime
from langchain_core.messages import SystemMessage
from sqlalchemy.orm import Session
from src.loan_sales_agent_shared.config import LLM

from src.agent.utils.pdf_generator import generate_sanction_letter_pdf
from src.loan_sales_agent_DL.repository.loan_application_repository import create_loan_application
from agent.state_and_graph.state import LoanState
from src.loan_sales_agent_BL.schemas.loan_application_schema import LoanApplicationCreate


class SanctionAgent:
    def __init__(self, db: Session):
        self.db = db
        self.llm_with_tools = LLM

    def sanction_letter(self, state: LoanState) -> LoanState:
        application_id = str(uuid.uuid4())[:8].upper()
        state['application_id'] = f'APP{datetime.datetime.year}{application_id}'

        app_data = LoanApplicationCreate(
            conversation_id=state['conversation_id'],
            conversation_history=state['messages'],
            loan_amount=state['loan_amount'],
            tenure_months=state['tenure_months'],
            interest_rate=state['interest_rate'],
            monthly_emi=state['monthly_emi'],
            status="approved",
            rejection_reason=None,
        )
        
        create_loan_application(self.db, state['customer_id'], app_data)

        llm_with_tools = self.llm_with_tools.bind_tools([generate_sanction_letter_pdf])
 
        system_msg = f"""You are a worker loan sales agent. Your job is to generate the 
        sanction letter by tool calling and send a proper goodbye greeting to the customer 
        {state['customer_name']} and ask them to visit again."""
 
        response = llm_with_tools.invoke([SystemMessage(content=system_msg)])
        
        state['messages'].append(response)
        state['next_action'] = "end"
 
        return state
