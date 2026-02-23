from langchain_ollama import ChatOllama
from dotenv import load_dotenv
import os

load_dotenv()

MODEL = "qwen2.5:7b"

LLM = ChatOllama(
    model = MODEL,
    temperature=0.2,
    num_predict=512,
    top_p=0.8,
    top_k=20
)

path = "agent/utils/sanction_letters"
os.makedirs(path, exist_ok=True)
SANCTION_LETTER_DIR = path