from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from config import LLM
from workflow.state import LoanState

class SalesAgent:
    def __init__(self):
        self.llm = LLM

    def negotiate_loan(self, state: LoanState):
        customer_data = state.get('customer_data', {})
        pre_approved = state.get('pre_approved_limit', 0)

        system_msg = f"""You are a loan sales specialist. The customer {customer_data.get('name')}
        has a pre-approved limit of ₹{pre_approved: .0f}.

        Dicuss their loan needs:
        - Desired loan amount
        - Purpose of loan
        - Prefered tennure (12 to 60 months)

        Be persuasive but honest. Offer competitive interest rate (9.5% - 12.5% based on profile).
        Calculate and present EMI options"""

        last_msg = state['messages'][-1] if state['messages'] else ""
        human_msg = f"""{last_msg.content if hasattr(last_msg, 'content') else last_msg}"""

        response = self.llm.invoke([
            SystemMessage(content=system_msg),
            HumanMessage(content=human_msg)
        ])

        state['messages'].append(response.content)

        if state.get('loan_amount') and state.get('tenure_months'):
            state['next_action'] = "verification"
        else:
            state['next_action'] = 'continue_sales'

        return state
    
