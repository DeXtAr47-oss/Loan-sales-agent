from langgraph.graph import END

from src.agent.states.state import LoanState
from src.agent.master_agent.master_agent import MasterAgent
from src.agent.graphs.create_workflow import WorkflowBuilder

from sqlalchemy.orm import Session

def create_master_agent_workflow(db: Session):
    master_agent = MasterAgent()

    workflow = WorkflowBuilder().workflow

    workflow.add_node("master_start", master_agent.start_conversation)
    workflow.add_node("master_end", master_agent.end_conversation)

    def route_after_start(state: LoanState) -> str:
        if state.get("customer_email") and state.get("customer_data"):
            return "verification"
        return END

    workflow.set_entry_point("master_start")
    workflow.add_conditional_edges("master_start", route_after_start)
    workflow.add_edge("master_end", END)

    return workflow.compile()



