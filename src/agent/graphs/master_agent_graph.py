from langgraph.graph import END
from src.agent.states.state import LoanState
from src.agent.master_agent.master_agent import MasterAgent
from src.agent.sales_agent.sales_agent import SalesAgent
from src.agent.graphs.create_workflow import WorkflowBuilder

def create_master_agent_workflow():
    master_agent = MasterAgent()
    sales_agent = SalesAgent()

    workflow = WorkflowBuilder().workflow

    # Nodes
    workflow.add_node(
        "master_start",
        master_agent.start_conversation
    )

    workflow.add_node(
        "get_customer_requirement",
        sales_agent.get_customer_requirements
    )

    workflow.add_node(
        "master_end",
        master_agent.end_conversation
    )

    #
    # Routing from Master Agent
    #
    def route_after_start(state: LoanState):

        next_action = state.get("next_action")

        if next_action == "get_customer_requirement":
            return "get_customer_requirement"

        if next_action == "end":
            return "master_end"

        return END

    #
    # Routing from Sales Agent
    #
    def route_after_get_customer_requirement(state: LoanState):

        # Hand control back to master
        return "master_start"

    #
    # Edges
    #
    workflow.set_entry_point("master_start")

    workflow.add_conditional_edges(
        "master_start",
        route_after_start
    )

    workflow.add_conditional_edges(
        "get_customer_requirement",
        route_after_get_customer_requirement
    )

    workflow.add_edge(
        "master_end",
        END
    )

    return workflow.compile()



