from __future__ import annotations

from dataclasses import dataclass, replace

from backend.rag.config import DEFAULT_CONFIG, RagConfig
from backend.rag.vectordb import get_collection, rebuild_index


@dataclass(frozen=True)
class RetrievedChunk:
    page_content: str
    metadata: dict
    distance: float | None = None


def retrieve(
    question: str,
    top_k: int | None = None,
    config: RagConfig = DEFAULT_CONFIG,
) -> list[RetrievedChunk]:
    question = question.strip()
    if not question:
        raise ValueError("question cannot be empty")

    collection = get_collection(config)
    result = collection.query(
        query_texts=[question],
        n_results=top_k or config.top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = result.get("documents", [[]])[0] or []
    metadatas = result.get("metadatas", [[]])[0] or []
    distances = result.get("distances", [[]])[0] or []

    return [
        RetrievedChunk(page_content=document, metadata=metadata or {}, distance=distance)
        for document, metadata, distance in zip(documents, metadatas, distances)
    ]


def compare_retrieval_quality(
    question: str,
    config: RagConfig = DEFAULT_CONFIG,
) -> dict[str, list[RetrievedChunk]]:
    results: dict[str, list[RetrievedChunk]] = {}

    for strategy in ("fixed", "recursive"):
        strategy_config = replace(
            config,
            collection_name=f"{config.collection_name}_{strategy}",
            chunk_strategy=strategy,
        )
        rebuild_index(strategy_config)
        results[strategy] = retrieve(question, config=strategy_config)

    return results
