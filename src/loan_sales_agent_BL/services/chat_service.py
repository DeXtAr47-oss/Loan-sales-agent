from src.agent.states.state import LoanState
from src.loan_sales_agent_BL.schemas.chat_schema import ChatResponse, ChatRequest


async def chat_service(graph, chat_request: ChatRequest, current_user):

    if chat_request.message.strip():
        initial_state: LoanState = {
            "messages": [
                {
                    "role": "user",
                    "content": chat_request.message
                }
            ]
        }
    else:
        initial_state: LoanState = {
            "messages": []
        }

    if current_user:
        thread_id = str(current_user.customer_id)
    else:
        thread_id = chat_request.thread_id or "anonymous"

    result = await graph.ainvoke(
        initial_state,
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    last_message = result["messages"][-1]

    return ChatResponse(
        reply=(
            last_message.content
            if hasattr(last_message, "content")
            else str(last_message)
        ),
        state=dict(result)
    )
