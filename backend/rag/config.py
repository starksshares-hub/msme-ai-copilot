from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RagConfig:
    knowledge_base_path: Path = Path(os.getenv("MSME_RAG_KNOWLEDGE_BASE", "knowledge_base"))
    chroma_path: Path = Path(os.getenv("MSME_RAG_CHROMA_PATH", "chroma_db"))
    collection_name: str = os.getenv("MSME_RAG_COLLECTION", "msme_knowledge_base")
    embedding_provider: str = os.getenv("MSME_RAG_EMBEDDING_PROVIDER", "huggingface")
    embedding_model_name: str = os.getenv("MSME_RAG_EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    chunk_strategy: str = os.getenv("MSME_RAG_CHUNK_STRATEGY", "recursive")
    chunk_size: int = int(os.getenv("MSME_RAG_CHUNK_SIZE", "1200"))
    chunk_overlap: int = int(os.getenv("MSME_RAG_CHUNK_OVERLAP", "150"))
    top_k: int = int(os.getenv("MSME_RAG_TOP_K", "5"))
    ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
    ollama_timeout_seconds: float = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60"))


DEFAULT_CONFIG = RagConfig()
