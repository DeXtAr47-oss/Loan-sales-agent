from langchain_ollama import ChatOllama
import os

# LLM config
MODEL = "qwen2.5:7b"
LLM = ChatOllama(
    model = MODEL,
    temperature=0.2,
    num_predict=512,
    top_p=0.8,
    top_k=20
)

# Sanction letter stored path
path = "agent/utils/sanction_letters"
os.makedirs(path, exist_ok=True)
SANCTION_LETTER_DIR = path

# Database Config
POSTGRES_CONFIG = {
    "host": os.getenv('POSTGRES_HOST', 'localhost'),
    "port": os.getenv('POSTGRES_PORT', '5432'),
    "database": os.getenv('POSTGRES_DB', 'nbfc_database'),
    "user": os.getenv('POSTGRES_USER', 'nbfc_user'),
    "password": os.getenv('POSTGRES_PASSWORD', 'nbfc123')
}
DATABASE_URL = f"postgresql://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{POSTGRES_CONFIG['database']}"
TEST_DATABASE_URL = f"postgresql://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/nbfc_test_database"
DB_PATH = "databases/data/"
os.makedirs(DB_PATH, exist_ok=True)