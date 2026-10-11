
"""Session 8 helpers: chat model, embedding model and vector store."""
import hashlib
import math
import os
import re

from dotenv import load_dotenv
from langchain_core.embeddings import Embeddings

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "ollama").strip().lower()
EMBED_PROVIDER = os.getenv(
    "EMBED_PROVIDER",
    "ollama" if PROVIDER == "ollama" else "fastembed"
).strip().lower()

DB_DIR = "chroma_db"
COLLECTION = "college_helpdesk"


def get_model(temperature=0):
    """Return the configured chat model."""
    if PROVIDER == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=os.getenv("MODEL", "qwen2.5:1.5b"),
            temperature=temperature
        )

    if PROVIDER == "groq":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY"),
            model=os.getenv("MODEL", "openai/gpt-oss-20b"),
            temperature=temperature
        )

    if PROVIDER == "huggingface":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            base_url="https://router.huggingface.co/v1",
            api_key=os.getenv("HF_TOKEN"),
            model=os.getenv("MODEL", "openai/gpt-oss-20b"),
            temperature=temperature
        )

    raise SystemExit(
        f"Unknown PROVIDER '{PROVIDER}'. "
        "Use ollama, groq or huggingface."
    )


class HashEmbeddings(Embeddings):
    """Offline keyword-based embedding fallback."""

    STOP = set(
        "a an the is are was to of in on for and or by at be it "
        "this that with what how do does i my can".split()
    )

    def _vec(self, text):
        vector = [0.0] * 256

        for word in re.findall(r"[a-z0-9]+", text.lower()):
            if word in self.STOP:
                continue

            if word.endswith("s") and len(word) > 3:
                word = word[:-1]

            index = int(hashlib.md5(word.encode()).hexdigest(), 16) % 256
            vector[index] += 1.0

        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

    def embed_documents(self, texts):
        return [self._vec(text) for text in texts]

    def embed_query(self, text):
        return self._vec(text)


def get_embeddings():
    """Return the selected embedding model."""

    if EMBED_PROVIDER == "ollama":
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(
            model=os.getenv("EMBED_MODEL", "nomic-embed-text")
        )

    if EMBED_PROVIDER == "fastembed":
        from langchain_community.embeddings import FastEmbedEmbeddings

        # Use FastEmbed's default supported model configuration.
        return FastEmbedEmbeddings()

    if EMBED_PROVIDER == "hash":
        return HashEmbeddings()

    raise SystemExit(
        f"Unknown EMBED_PROVIDER '{EMBED_PROVIDER}'. "
        "Use ollama, fastembed or hash."
    )


def get_vectorstore():
    """Open or create the persistent Chroma collection."""
    from langchain_chroma import Chroma

    return Chroma(
        collection_name=COLLECTION,
        embedding_function=get_embeddings(),
        persist_directory=DB_DIR,
        collection_metadata={"hnsw:space": "cosine"}
    )
