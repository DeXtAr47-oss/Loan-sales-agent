from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.loan_sales_agent_API.Customer_controller import router, api_router
from src.loan_sales_agent_API.Chat_controller import chat_router
from src.loan_sales_agent_API.Credit_score_controller import credit_score_api_router
from src.loan_sales_agent_API.Signin_controller import signin_router, api_signin_router
from src.loan_sales_agent_DL import *
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(api_router)
app.include_router(credit_score_api_router)
app.include_router(chat_router)
app.include_router(api_signin_router)
app.include_router(signin_router)
app.mount(
    "/static",
    StaticFiles(directory="frontend/build/static"),
    name="static"
)

# SERVE REACT APP
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    return FileResponse("frontend/build/index.html")
