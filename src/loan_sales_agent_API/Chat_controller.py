from fastapi import APIRouter, Depends, Request, UploadFile
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

from src.loan_sales_agent_shared.config import CHECKPOINTER_DATABASE_URL
from src.loan_sales_agent_shared.connection import get_db
from src.loan_sales_agent_BL.services.chat_service import chat_service
from src.loan_sales_agent_BL.schemas.chat_schema import ChatResponse, ChatRequest
from src.loan_sales_agent_BL.services.authentication_service import get_current_user_api
from src.agent.graphs.graph import create_loan_workflow

@asynccontextmanager
async def lifespan(app):
    async with AsyncPostgresSaver.from_conn_string(CHECKPOINTER_DATABASE_URL) as checkpointer:
        await checkpointer.setup()
        app.state.graph = await create_loan_workflow(checkpointer)
        yield
        app.state.graph = None

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    include_in_schema=False
)

api_chat_router = APIRouter(
    prefix="/api/chat",
    tags=["Chat API"]
)

@chat_router.post("", response_model=ChatResponse)
async def chat(
    request: Request,
    current_user=Depends(get_current_user_api),
):
    graph = request.app.state.graph
    content_type = request.headers.get("content-type", "")

    file: UploadFile | None = None
    if content_type.startswith("multipart/form-data"):
        form = await request.form()
        message = str(form.get("message") or "")
        thread_id = form.get("thread_id")
        uploaded_file = form.get("file")
        if hasattr(uploaded_file, "filename") and hasattr(uploaded_file, "read"):
            file = uploaded_file
    else:
        payload = await request.json()
        message = payload.get("message") or ""
        thread_id = payload.get("thread_id")

    chat_request = ChatRequest(
        message=message,
        thread_id=str(thread_id) if thread_id else None,
    )
    return await chat_service(graph, chat_request, current_user, file)

@api_chat_router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest,
               http_request: Request,
               current_user = Depends(get_current_user_api)):
    graph = http_request.app.state.graph
    return await chat_service(graph, request, current_user, None)
