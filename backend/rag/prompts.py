from __future__ import annotations

from backend.rag.retriever import RetrievedChunk


SYSTEM_PROMPT = """You are an MSME Finance AI Copilot.

Always answer only using retrieved business documents.

If insufficient information exists, explicitly say so."""


def build_context(chunks: list[RetrievedChunk]) -> str:
    if not chunks:
        return "No retrieved context."

    context_blocks = []
    for index, chunk in enumerate(chunks, start=1):
        source = chunk.metadata.get("relative_path") or chunk.metadata.get("source_file")
        context_blocks.append(
            f"[{index}] Source: {source}\n{chunk.page_content}"
        )

    return "\n\n".join(context_blocks)


def build_messages(question: str, chunks: list[RetrievedChunk]) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "Retrieved business documents:\n"
                f"{build_context(chunks)}\n\n"
                f"User question:\n{question}\n\n"
                "Answer with the shortest useful response and cite only the listed sources."
            ),
        },
    ]
