from langgraph.graph import StateGraph
from src.agent.states.state import LoanState

class WorkflowBuilder:
    _instance: "WorkflowBuilder | None" = None
    _workflow: StateGraph | None = None

    def __new__(cls) -> "WorkflowBuilder":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def workflow(self) -> StateGraph:
        if self._workflow is None:
            self._workflow = StateGraph(LoanState)
        return self._workflow