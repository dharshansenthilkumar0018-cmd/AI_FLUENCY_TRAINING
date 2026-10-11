import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "ollama").lower()
MODEL = os.getenv("MODEL", "qwen2.5:1.5b")
BASE_URL = os.getenv("BASE_URL", "http://localhost:11434/v1")
API_KEY = os.getenv("API_KEY", "ollama")
EMBED_PROVIDER = os.getenv("EMBED_PROVIDER", "ollama").lower()
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
MAX_DISTANCE = float(os.getenv("MAX_DISTANCE", "0.6"))

def get_embeddings():
    if EMBED_PROVIDER == "ollama":
        return OllamaEmbeddings(model=EMBED_MODEL)
    return OpenAIEmbeddings(
        model=EMBED_MODEL,
        base_url=BASE_URL,
        api_key=API_KEY
    )

def get_llm():
    return ChatOpenAI(
        model=MODEL,
        base_url=BASE_URL,
        api_key=API_KEY,
        temperature=0
    )

def get_store():
    return Chroma(
        collection_name="college_handbook",
        persist_directory="chroma_db",
        embedding_function=get_embeddings(),
        collection_metadata={"hnsw:space": "cosine"}
    )
