import uuid
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from .config import LLM
from .workflow.state import LoanState

class MasterAgent:
    def __init__(self):
        self.llm = LLM

    def start_conversation(self, state: LoanState) -> LoanState:
        if not state.get("conversation_id"):
            state['conversation_id'] = str(uuid.uuid4())

        system_msg = """You are a friendly and professional loan sales agent, your goal is to warmly greet the customer and understood their loan requirements."""

        response = self.llm.invoke([SystemMessage(content = system_msg)])
        state['messages'] = [AIMessage(content=response.content)]
        state['next_action'] = 'await_customer_info'

        return state
    
    def end_conversation(self, state: LoanState) -> LoanState:
        if state["final_status"] == "rejected":
            closing_msg = f"""Unfortunately, your application could not be approved at this time due to:
                            {state.get('rejection_reason')}

                            You may reapply after 3 months or contact our customer service for alternative options.

                            Thank you for your time! 🙏"""
            
        else:
            closing_msg = """Thank you for completing your loan application with us! 

                        Our team will contact you shortly for the next steps. Have a great day! 😊"""
        
        state["messages"].append(AIMessage(content=closing_msg))
            
        return state