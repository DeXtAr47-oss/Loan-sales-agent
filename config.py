from langchain_ollama import ChatOllama
import os
from dotenv import load_dotenv

load_dotenv()

# LLM config
LLM = ChatOllama(
    model = os.getenv("MDOEL"),
    temperature=0.2,
    num_predict=512,
    top_p=0.8,
    top_k=20
)

# Sanction letter stored path
os.makedirs(os.getenv("SANCTION_LETTER_PATH"), exist_ok=True)
SANCTION_LETTER_PATH = os.getenv("SANCTION_LETTER_PATH")

# Database Config
DATABASE_URL = f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/{os.getenv("POSTGRES_DATABASE")}"
TEST_DATABASE_URL = f"postgresql://{os.getenv("POSTGRES_USER")}:{os.getenv("POSTGRES_PASSWORD")}@{os.getenv("POSTGRES_HOST")}:{os.getenv("POSTGRES_PORT")}/nbfc_test_database"
os.makedirs(os.getenv("DB_PATH"), exist_ok=True)