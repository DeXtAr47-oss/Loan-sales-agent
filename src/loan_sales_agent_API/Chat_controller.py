from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.loan_sales_agent_shared.connection import get_db
from src.loan_sales_agent_BL.services.chat_service import chat_service
from src.loan_sales_agent_BL.schemas.chat_schema import ChatResponse, ChatRequest
from src.loan_sales_agent_BL.services.authentication_service import get_current_user, get_current_user_api

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
async def chat(request: ChatRequest,
               http_request: Request,
               db: AsyncSession = Depends(get_db),
               current_user = Depends(get_current_user_api)
               ):
    graph = http_request.app.state.graph
    return await chat_service(graph, request, current_user)

@api_chat_router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest,
               http_request: Request,
               db: AsyncSession = Depends(get_db),
               current_user = Depends(get_current_user_api)):
    graph = http_request.app.state.graph
    return await chat_service(graph, request, current_user)