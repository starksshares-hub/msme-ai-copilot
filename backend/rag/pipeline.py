from __future__ import annotations

import argparse
from dataclasses import dataclass

import ollama

from backend.rag.config import DEFAULT_CONFIG, RagConfig
from backend.rag.prompts import build_messages
from backend.rag.retriever import RetrievedChunk, compare_retrieval_quality, retrieve
from backend.rag.vectordb import rebuild_index


@dataclass(frozen=True)
class RagAnswer:
    answer: str
    sources: list[str]
    chunks: list[RetrievedChunk]


def generate_answer(messages: list[dict[str, str]], config: RagConfig = DEFAULT_CONFIG) -> str:
    client = ollama.Client(timeout=config.ollama_timeout_seconds)

    try:
        response = client.chat(model=config.ollama_model, messages=messages)
    except Exception as exc:
        raise RuntimeError(
            f"Failed to generate answer with Ollama model {config.ollama_model}. "
            "Make sure Ollama is running and the model is installed."
        ) from exc

    message = response.get("message") if isinstance(response, dict) else response.message
    content = message.get("content") if isinstance(message, dict) else message.content
    return content.strip()


def unique_sources(chunks: list[RetrievedChunk]) -> list[str]:
    sources: list[str] = []

    for chunk in chunks:
        source = chunk.metadata.get("relative_path") or chunk.metadata.get("source_file")
        if source and source not in sources:
            sources.append(source)

    return sources


def answer_question(question: str, config: RagConfig = DEFAULT_CONFIG) -> RagAnswer:
    chunks = retrieve(question, top_k=config.top_k, config=config)

    if not chunks:
        return RagAnswer(
            answer="Insufficient information exists in the retrieved business documents.",
            sources=[],
            chunks=[],
        )

    messages = build_messages(question, chunks)
    answer = generate_answer(messages, config=config)
    return RagAnswer(answer=answer, sources=unique_sources(chunks), chunks=chunks)


def format_answer(result: RagAnswer) -> str:
    sources = "\n".join(f"- {source}" for source in result.sources)
    if not sources:
        sources = "- No sources"

    return f"{result.answer}\n\nSources:\n{sources}"


def print_comparison(question: str, config: RagConfig = DEFAULT_CONFIG) -> None:
    results = compare_retrieval_quality(question, config=config)

    for strategy, chunks in results.items():
        print(f"\n{strategy.upper()} chunking")
        for chunk in chunks:
            source = chunk.metadata.get("relative_path") or chunk.metadata.get("source_file")
            distance = "n/a" if chunk.distance is None else f"{chunk.distance:.4f}"
            print(f"- distance={distance} source={source}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run MSME RAG question answering")
    parser.add_argument("question", nargs="*", help="User question")
    parser.add_argument("--ingest", action="store_true", help="Rebuild the local ChromaDB index")
    parser.add_argument("--compare", action="store_true", help="Compare fixed vs recursive retrieval")
    args = parser.parse_args()

    question = " ".join(args.question).strip()

    if args.ingest:
        count = rebuild_index(DEFAULT_CONFIG)
        print(f"Ingested {count} chunks into {DEFAULT_CONFIG.collection_name}")

    if args.compare:
        if not question:
            raise SystemExit("--compare requires a question")
        print_comparison(question)
        return

    if question:
        try:
            print(format_answer(answer_question(question)))
        except RuntimeError as exc:
            raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
