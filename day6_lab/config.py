"""Shared configuration for Day 6.

Set PROVIDER and MODEL in .env.
Examples:
  PROVIDER=ollama
  MODEL=qwen2.5:1.5b
  OLLAMA_BASE_URL=http://localhost:11434/v1

For Groq:
  PROVIDER=groq
  MODEL=<a model available to your Groq account>
  GROQ_API_KEY=<your key>
  GROQ_BASE_URL=https://api.groq.com/openai/v1
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "ollama").lower()
MODEL = os.getenv("MODEL", "qwen2.5:1.5b")

if PROVIDER == "ollama":
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    api_key = os.getenv("OLLAMA_API_KEY", "ollama")
elif PROVIDER == "groq":
    base_url = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY is required when PROVIDER=groq")
elif PROVIDER in {"huggingface", "hf"}:
    base_url = os.getenv(
        "HF_BASE_URL",
        "https://router.huggingface.co/v1",
    )
    api_key = os.getenv("HF_TOKEN")
    if not api_key:
        raise RuntimeError("HF_TOKEN is required when PROVIDER=huggingface")
else:
    base_url = os.getenv("BASE_URL")
    api_key = os.getenv("API_KEY")
    if not base_url or not api_key:
        raise RuntimeError(
            "Unknown provider. Set BASE_URL and API_KEY in .env."
        )

client = OpenAI(base_url=base_url, api_key=api_key)

def banner(title: str) -> None:
    print(f"\n=== {title} | provider: {PROVIDER} | model: {MODEL} ===\n")
