from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_KNOWLEDGE_BASE = Path("knowledge_base")


@dataclass(frozen=True)
class KnowledgeDocument:
    page_content: str
    metadata: dict[str, str]


def iter_markdown_files(
    knowledge_base_path: str | Path = DEFAULT_KNOWLEDGE_BASE,
) -> list[Path]:
    knowledge_base = Path(knowledge_base_path)

    if not knowledge_base.exists():
        raise FileNotFoundError(f"Knowledge base folder not found: {knowledge_base}")

    if not knowledge_base.is_dir():
        raise NotADirectoryError(f"Knowledge base path is not a folder: {knowledge_base}")

    return sorted(
        file_path
        for file_path in knowledge_base.rglob("*.md")
        if file_path.is_file()
    )


def load_documents(
    knowledge_base_path: str | Path = DEFAULT_KNOWLEDGE_BASE,
) -> list[KnowledgeDocument]:
    knowledge_base = Path(knowledge_base_path)
    documents: list[KnowledgeDocument] = []

    for file_path in iter_markdown_files(knowledge_base):
        relative_path = file_path.relative_to(knowledge_base)

        documents.append(
            KnowledgeDocument(
                page_content=file_path.read_text(encoding="utf-8"),
                metadata={
                    "file_name": file_path.name,
                    "source_file": file_path.name,
                    "relative_path": relative_path.as_posix(),
                    "source_path": str(file_path),
                },
            )
        )

    return documents


def main() -> None:
    documents = load_documents()

    print(f"Loaded {len(documents)} Markdown files from {DEFAULT_KNOWLEDGE_BASE}")
    for document in documents:
        print(document.metadata["relative_path"])


if __name__ == "__main__":
    main()
