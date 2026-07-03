from __future__ import annotations

import chromadb

from backend.rag.chunker import DocumentChunk, chunk_documents
from backend.rag.config import DEFAULT_CONFIG, RagConfig
from backend.rag.embeddings import get_embedding_function
from backend.rag.loader import load_documents


def get_client(config: RagConfig = DEFAULT_CONFIG):
    config.chroma_path.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(config.chroma_path))


def collection_exists(client, collection_name: str) -> bool:
    return any(
        getattr(collection, "name", collection) == collection_name
        for collection in client.list_collections()
    )


def get_collection(config: RagConfig = DEFAULT_CONFIG):
    client = get_client(config)
    return client.get_or_create_collection(
        name=config.collection_name,
        embedding_function=get_embedding_function(config),
        metadata={
            "embedding_provider": config.embedding_provider,
            "embedding_model": config.embedding_model_name,
            "chunk_strategy": config.chunk_strategy,
        },
    )


def reset_collection(config: RagConfig = DEFAULT_CONFIG):
    client = get_client(config)
    if collection_exists(client, config.collection_name):
        client.delete_collection(config.collection_name)

    return client.get_or_create_collection(
        name=config.collection_name,
        embedding_function=get_embedding_function(config),
        metadata={
            "embedding_provider": config.embedding_provider,
            "embedding_model": config.embedding_model_name,
            "chunk_strategy": config.chunk_strategy,
        },
    )


def upsert_chunks(
    chunks: list[DocumentChunk],
    config: RagConfig = DEFAULT_CONFIG,
    reset: bool = False,
) -> int:
    collection = reset_collection(config) if reset else get_collection(config)

    if not chunks:
        return 0

    collection.upsert(
        ids=[chunk.metadata["chunk_id"] for chunk in chunks],
        documents=[chunk.page_content for chunk in chunks],
        metadatas=[chunk.metadata for chunk in chunks],
    )

    return len(chunks)


def rebuild_index(config: RagConfig = DEFAULT_CONFIG) -> int:
    documents = load_documents(config.knowledge_base_path)
    chunks = chunk_documents(
        documents=documents,
        strategy=config.chunk_strategy,
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
    )

    return upsert_chunks(chunks, config=config, reset=True)
