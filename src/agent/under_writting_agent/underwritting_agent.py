from langchain.messages import AIMessage
from sqlalchemy.orm import Session

from src.loan_sales_agent_shared.config import MIN_CREDIT_SCORE, EMI_TO_SALARY_RATIO
from agent.state_and_graph.state import LoanState
from src.loan_sales_agent_DL.repository.credit_score_repository import get_credit_score, update_credit_score
from src.loan_sales_agent_DL.repository.loan_application_repository import update_conversation_history
from src.loan_sales_agent_BL.schemas.loan_application_schema import LoanApplicationCreate


class UnderwrittingAgent:
    def __init__(self, db: Session):
        self.db = db

    def access_credit_worthiness(self, state: LoanState) -> LoanState:
        customer_id = state.get('customer_id')
        loan_amount = state.get('loan_amount', 0)
        pre_approved_limit = state.get('pre_approved_limit', 0)
        tenure = state.get('tenure_months', 36)

        credit_score = get_credit_score(self.db, state['customer_id'])
        state['credit_score'] = credit_score
        update_credit_score(self.db, customer_id, credit_score)
        state['credit_check_done'] = True

        interest_rate = state.get("interest_rate", 10.5)
        monthly_rate = interest_rate / (12 * 100)
        emi = loan_amount * monthly_rate * ((1 + monthly_rate) ** tenure) / (((1 + monthly_rate) ** tenure) - 1)
        state["monthly_emi"] = round(emi, 2)

        if credit_score < MIN_CREDIT_SCORE:
            state["under_writing_approved"] = False
            state["final_status"] = "rejected"
            state["rejection_reason"] = f"Credit score {credit_score} below minimum requirement of {MIN_CREDIT_SCORE}"
            state["next_action"] = "rejected"
            
        elif loan_amount <= pre_approved_limit:
            state["under_writing_approved"] = True
            state["final_status"] = "approved"
            state["next_action"] = "generate_sanction_letter"
            
        elif loan_amount <= 2 * pre_approved_limit:
            if not state.get("salary_slip_uploaded"):
                state["next_action"] = "request_salary_slip"
            else:
                salary = state.get("salary_amount", 0)
                if emi <= EMI_TO_SALARY_RATIO * salary:
                    state["under_writing_approved"] = True
                    state["final_status"] = "approved"
                    state["next_action"] = "generate_sanction_letter"
                else:
                    state["under_writing_approved"] = False
                    state["final_status"] = "rejected"
                    state["rejection_reason"] = f"EMI ₹{emi:,.0f} exceeds 50% of monthly salary ₹{salary:,.0f}"
                    state["next_action"] = "rejected"
        else:
            state["under_writing_approved"] = False
            state["final_status"] = "rejected"
            state["rejection_reason"] = f"Loan amount ₹{loan_amount:,.0f} exceeds 2x pre-approved limit ₹{pre_approved_limit:,.0f}"
            state["next_action"] = "rejected"

        underwriting_msg = f"""Credit Assessment Complete

Credit Score: {credit_score}/900
Loan Amount: ₹{loan_amount:,.0f}
Tenure: {tenure} months
Interest Rate: {interest_rate}%
Monthly EMI: ₹{emi:,.2f}

Pre-approved Limit: ₹{pre_approved_limit:,.0f}"""
        
        state["messages"].append(AIMessage(content=underwriting_msg))

        app_data = LoanApplicationCreate(conversation_history=state['messages'])
        update_conversation_history(self.db, customer_id, app_data)
        return state