from langgraph.graph import StateGraph, END

from src.loan_sales_agent_shared.config import DATABASE_URL
from agent.state_and_graph.state import LoanState
from src.agent.master_agent.master_agent import MasterAgent
from src.agent.sales_agent.sales_agent import SalesAgent
from src.agent.verification_agent.verification_agent import VerificationAgent
from src.agent.under_writting_agent.underwritting_agent import UnderwrittingAgent
from src.agent.sanction_agent.sanction_agent import SanctionAgent

from sqlalchemy.orm import Session

def create_loan_workflow(db: Session):
    """Create and compile the LangGraph workflow with PostgreSQL checkpointing"""
    
    # Initialize agents
    master_agent = MasterAgent()
    sales_agent = SalesAgent()
    verification_agent = VerificationAgent()
    underwriting_agent = UnderwrittingAgent(db)
    sanction_agent = SanctionAgent(db)
    
    # Define the graph
    workflow = StateGraph(LoanState)
    
    # Add nodes
    workflow.add_node("master_start", master_agent.start_conversation)
    workflow.add_node("verify_customer", verification_agent.verify_customer)
    workflow.add_node("sales", sales_agent.negotiate_loan)
    workflow.add_node("verification", verification_agent.verify_kyc)
    workflow.add_node("underwriting", underwriting_agent.acess_credit_worthiness)
    workflow.add_node("sanction_letter", sanction_agent.sanction_letter)
    workflow.add_node("master_end", master_agent.end_conversation)
    
    # Define routing functions
    def route_after_start(state: LoanState) -> str:
        if state.get("customer_email") and state.get("customer_data"):
            return "sales"
        return END
    
    def route_after_sales(state: LoanState) -> str:
        if state.get("loan_amount") and state.get("tenure_months"):
            return "verification"
        return END
    
    def route_after_underwriting(state: LoanState) -> str:
        next_action = state.get("next_action")
        if next_action == "generate_sanction_letter":
            return "sanction_letter"
        elif next_action == "rejected":
            return "master_end"
        elif next_action == "request_salary_slip":
            return "underwriting"
        return "master_end"
    
    # Define edges
    workflow.set_entry_point("master_start")
    workflow.add_conditional_edges("master_start", route_after_start)
    workflow.add_conditional_edges("sales", route_after_sales)
    workflow.add_edge("verification", "underwriting")
    workflow.add_conditional_edges("underwriting", route_after_underwriting)
    workflow.add_edge("sanction_letter", "master_end")
    workflow.add_edge("master_end", END)
    
    # Setup PostgreSQL checkpointer for state persistence
    # This uses the SAME PostgreSQL database for checkpoint storage
    print("[System] Using PostgreSQL for LangGraph state checkpointing...")
    
    try:
        # Create PostgresSaver with connection string
        memory = PostgresSaver.from_conn_string(DATABASE_URL)
        
        # Setup checkpoint table if it doesn't exist
        memory.setup()
        
        print("✓ PostgreSQL checkpoint storage initialized")
    except Exception as e:
        print(f"✗ Error setting up PostgreSQL checkpointing: {e}")
        print("  Falling back to in-memory state (no persistence)")
        memory = None
    
    # Compile the graph with PostgreSQL checkpointing
    app = workflow.compile(checkpointer=memory)
    
    return app