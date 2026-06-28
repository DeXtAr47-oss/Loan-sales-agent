from langchain_ollama import ChatOllama, OllamaEmbeddings
from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
from pinecone import Pinecone
from passlib.context import CryptContext
from pathlib import Path

load_dotenv()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# LLM config
LLM = ChatOllama(
    model = os.getenv("MODEL"),
    temperature=0.2,
    num_predict=200,
    top_p=0.8,
    top_k=20
)

# Embedding model config
EMBEDDING_MODEL = OllamaEmbeddings(
    model = os.getenv('EMBEDDING'),
    dimensions=1536
)

# Tool model config
TOOL_MODEL = ChatOllama(
    model = os.getenv('MODEL'),
    temperature=0.0,
    num_predict=1024,
    top_p=0.9,
    top_k=20,           
    num_ctx=4096,
    repeat_penalty=1.3,
)

# Sanction letter stored path
os.makedirs(os.getenv("SANCTION_LETTER_PATH"), exist_ok=True)
SANCTION_LETTER_PATH = os.getenv("SANCTION_LETTER_PATH")

# Salary Slip stored path
SALARY_SLIP_DIR = Path("/Users/pritamdas/python/projects/loan-sales-agent/src/loan_sales_agent_shared/data/")

# Database Config
DATABASE_URL = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
CHECKPOINTER_DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
os.makedirs(os.getenv('DB_PATH'), exist_ok=True)

# Loan Configuration
INTEREST_RATE_RANGE = (9.5, 12.5)
MIN_CREDIT_SCORE = 700
MAX_CREDIT_SCORE = 900
MIN_TENURE_MONTHS = 12
MAX_TENURE_MONTHS = 60
EMI_TO_SALARY_RATIO = 0.5

# Vector Database
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
INDEX = pc.Index("nbfc-customer-memory")

# MCP
MCP = FastMCP('Loan sales agent')

# Authentication
AUTH_KEY = "loan_sales_agent_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30