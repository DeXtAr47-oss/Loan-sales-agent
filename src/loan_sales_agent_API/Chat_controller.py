from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.loan_sales_agent_shared.connection import get_db
from src.agent.graphs.master_agent_graph import create_master_agent_workflow
from src.agent.states.state import LoanState
from src.loan_sales_agent_BL.schemas.chat_schema import ChatResponse, ChatRequest

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@chat_router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    graph = create_master_agent_workflow(db)

    initial_state: LoanState = {
        "messages": [{"role": "user", "content": request.message}]
    }

    result = await graph.ainvoke(
        initial_state,
        config={"configurable": {"thread_id": request.thread_id}}
    )

    last_message = result["messages"][-1]

    return ChatResponse(
        reply=last_message.content if hasattr(last_message, "content") else str(last_message),
        state=dict(result)
    )