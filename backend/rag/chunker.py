from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from backend.rag.config import DEFAULT_CONFIG
from backend.rag.loader import KnowledgeDocument


ChunkStrategy = Literal["fixed", "recursive"]
RECURSIVE_SEPARATORS = ("\n\n", "\n", ". ", "; ", ", ", " ")


@dataclass(frozen=True)
class DocumentChunk:
    page_content: str
    metadata: dict[str, str | int]


def validate_chunk_settings(chunk_size: int, chunk_overlap: int) -> None:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if chunk_overlap < 0:
        raise ValueError("chunk_overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")


def fixed_chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CONFIG.chunk_size,
    chunk_overlap: int = DEFAULT_CONFIG.chunk_overlap,
) -> list[str]:
    validate_chunk_settings(chunk_size, chunk_overlap)
    text = text.strip()

    if not text:
        return []

    chunks: list[str] = []
    step = chunk_size - chunk_overlap

    for start in range(0, len(text), step):
        chunk = text[start : start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        if start + chunk_size >= len(text):
            break

    return chunks


def recursive_chunk_text(
    text: str,
    chunk_size: int = DEFAULT_CONFIG.chunk_size,
    chunk_overlap: int = DEFAULT_CONFIG.chunk_overlap,
) -> list[str]:
    validate_chunk_settings(chunk_size, chunk_overlap)
    chunks = _split_recursive(text.strip(), chunk_size, RECURSIVE_SEPARATORS)

    if chunk_overlap == 0 or len(chunks) <= 1:
        return chunks

    with_overlap = [chunks[0]]
    for previous, chunk in zip(chunks, chunks[1:]):
        prefix = previous[-chunk_overlap:].strip()
        with_overlap.append(f"{prefix}\n{chunk}".strip())

    return with_overlap


def _split_recursive(
    text: str,
    chunk_size: int,
    separators: tuple[str, ...],
) -> list[str]:
    if not text:
        return []

    if len(text) <= chunk_size:
        return [text]

    if not separators:
        return fixed_chunk_text(text, chunk_size, 0)

    separator = separators[0]
    pieces = text.split(separator)

    if len(pieces) == 1:
        return _split_recursive(text, chunk_size, separators[1:])

    chunks: list[str] = []
    current = ""

    for raw_piece in pieces:
        piece = raw_piece.strip()
        if not piece:
            continue

        candidate = f"{current}{separator}{piece}" if current else piece

        if len(candidate) <= chunk_size:
            current = candidate
            continue

        if current:
            chunks.append(current.strip())

        if len(piece) > chunk_size:
            chunks.extend(_split_recursive(piece, chunk_size, separators[1:]))
            current = ""
        else:
            current = piece

    if current:
        chunks.append(current.strip())

    return chunks


def chunk_documents(
    documents: list[KnowledgeDocument],
    strategy: str = DEFAULT_CONFIG.chunk_strategy,
    chunk_size: int = DEFAULT_CONFIG.chunk_size,
    chunk_overlap: int = DEFAULT_CONFIG.chunk_overlap,
) -> list[DocumentChunk]:
    if strategy not in {"fixed", "recursive"}:
        raise ValueError("strategy must be 'fixed' or 'recursive'")

    chunks: list[DocumentChunk] = []

    for document in documents:
        if strategy == "fixed":
            text_chunks = fixed_chunk_text(document.page_content, chunk_size, chunk_overlap)
        else:
            text_chunks = recursive_chunk_text(document.page_content, chunk_size, chunk_overlap)

        relative_path = document.metadata["relative_path"]

        for index, text_chunk in enumerate(text_chunks):
            chunk_id = f"{relative_path}::{strategy}::{index}"
            chunks.append(
                DocumentChunk(
                    page_content=text_chunk,
                    metadata={
                        **document.metadata,
                        "chunk_id": chunk_id,
                        "chunk_index": index,
                        "chunk_strategy": strategy,
                    },
                )
            )

    return chunks
