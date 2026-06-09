from langchain_ollama import ChatOllama, OllamaEmbeddings
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

# LLM config
LLM = ChatOllama(
    model = os.getenv("MODEL"),
    temperature=0.2,
    num_predict=512,
    top_p=0.8,
    top_k=20
)

# Sanction letter stored path
os.makedirs(os.getenv("SANCTION_LETTER_PATH"), exist_ok=True)
SANCTION_LETTER_PATH = os.getenv("SANCTION_LETTER_PATH")

# Database Config
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
TEST_DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/nbfc_test_database"
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

# Embedding model