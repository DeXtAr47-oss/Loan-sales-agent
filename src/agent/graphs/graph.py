from langgraph.graph import StateGraph, START, END

from src.loan_sales_agent_shared.config import DATABASE_URL
from src.agent.states.state import LoanState
from src.agent.master_agent.master_agent import MasterAgent
from src.agent.sales_agent.sales_agent import SalesAgent
from src.agent.verification_agent.verification_agent import VerificationAgent
from src.agent.under_writting_agent.underwritting_agent import UnderwritingAgent
from src.agent.sanction_agent.sanction_agent import SanctionAgent

async def create_loan_workflow(checkpointer):
    master_agent = MasterAgent()
    verification_agent = VerificationAgent()
    underwriting_agent = UnderwritingAgent()
    sanction_agent = SanctionAgent()

    workflow = StateGraph(LoanState)

    workflow.add_node("supervisor", master_agent.supervisor_node)
    workflow.add_node("sales", master_agent.sales_node)
    workflow.add_node("verification", verification_agent.verify_customer)
    workflow.add_node("underwriting", underwriting_agent.underwriting_node)
    workflow.add_node("sanction", sanction_agent.sanction_node)
    workflow.add_node("direct", master_agent.direct_node)

    workflow.add_edge(START, "supervisor")
    workflow.add_conditional_edges(
        "supervisor",
        master_agent.route,
        {
            "sales": "sales",
            "verification": "verification",
            "underwriting": "underwriting",
            "sanction": "sanction",
            "direct": "direct",
            "end": END,
        }
    )
    workflow.add_conditional_edges(
        "sales",
        master_agent.route_after_sales,
        {
            "verification": "verification",
            "end": END,
        }
    )
    workflow.add_conditional_edges(
        "verification",
        master_agent.route_after_verification,
        {
            "underwriting": "underwriting",
            "end": END,
        }
    )
    workflow.add_conditional_edges(
        "underwriting",
        master_agent.route_after_underwriting,
        {
            "sanction": "sanction",
            "end": END,
        }
    )
    workflow.add_edge("sanction", END)
    workflow.add_edge("direct", END)


    return workflow.compile(checkpointer=checkpointer)
