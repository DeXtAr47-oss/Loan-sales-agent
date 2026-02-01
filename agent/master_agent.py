import uuid
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from .config import MODEL
from .workflow.state import LoanState

class MasterAgent:
    def __init__(self):
        self.llm = MODEL

    def start_conversation(self, state: LoanState) -> LoanState:
        if not state.get("conversation_id"):
            state['conversation_id'] = str(uuid.uuid4())

        system_msg = """You are a friendly and professional loan sales agent, your goal is to warmly greet the customer and understood their loan requirements."""

        response = self.llm.invoke([SystemMessage(content = system_msg)])
        state['messages'] = [AIMessage(content=response.content)]
        state['next_action'] = 'await_customer_info'

        return state