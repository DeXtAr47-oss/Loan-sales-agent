from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.loan_sales_agent_API.Customer_controller import router, api_router
from src.loan_sales_agent_API.Chat_controller import chat_router, api_chat_router, lifespan
from src.loan_sales_agent_API.Credit_score_controller import credit_score_api_router
from src.loan_sales_agent_API.Signin_controller import signin_router, api_signin_router
from src.loan_sales_agent_API.Loan_offer_controller import loan_offer_router_api
from src.loan_sales_agent_shared.config import SANCTION_LETTER_PATH


app = FastAPI(lifespan=lifespan)

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
app.include_router(api_chat_router)
app.include_router(api_signin_router)
app.include_router(signin_router)
app.include_router(loan_offer_router_api)

app.mount(
    "/static",
    StaticFiles(directory="frontend/build/static"),
    name="static"
)


@app.get("/api/sanction-letter/{filename}", include_in_schema=False)
async def download_sanction_letter(filename: str):
    sanction_dir = Path(SANCTION_LETTER_PATH).resolve()
    file_path = (sanction_dir / filename).resolve()

    if file_path.parent != sanction_dir or file_path.suffix.lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Invalid sanction letter file")

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Sanction letter not found")

    return FileResponse(
        str(file_path),
        media_type="application/pdf",
        filename=filename,
    )

# SERVE REACT APP
@app.get("/{full_path:path}", include_in_schema=False)
async def serve_react_app(full_path: str):
    return FileResponse("frontend/build/index.html")
