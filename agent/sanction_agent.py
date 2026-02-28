import uuid
import datetime
from langchain_core.messages import AIMessage, SystemMessage
from config import LLM

from .utils.pdf_generator import generate_sanction_letter_pdf
from .workflow.state import LoanState

class SanctionAgent:
    def __init__(self, db):
        self.db = db
        self.llm_with_tools = LLM

    def sanction_letter(self, state: LoanState) -> LoanState:
        application_id = str(uuid.uuid4()[:8].upper())
        state['application_id'] = f'APP{datetime.datetime.year}{application_id}'

        #=============================
        # DATABASE CODE TO BE INSERTED
        #=============================

        self.llm_with_tools.bind(generate_sanction_letter_pdf)

        system_msg = f""" You are a worker loan sales agent, your job is to generate the sanction letter by tool calling and send a proper goodbye greeting
        to the customer {state['customer_name']} and say the customer to visit again. """

        response = self.llm_with_tools.invoke(SystemMessage(content=system_msg))
        state['messages'].append(response.content)
        state['next_action'] = "end"

        return state
