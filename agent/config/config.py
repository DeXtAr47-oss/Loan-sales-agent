from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

LLM = HuggingFaceEndpoint(
    repo_id='Qwen/Qwen2.5-7B-Instruct',
    task='text-generation',
    max_new_tokens=512,
    temperature=0.5,
    return_full_text=False,
    do_sample=False
)

MODEL = ChatHuggingFace(llm = LLM)