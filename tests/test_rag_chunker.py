import unittest

from backend.rag.chunker import chunk_documents, fixed_chunk_text, recursive_chunk_text
from backend.rag.loader import KnowledgeDocument


class RagChunkerTests(unittest.TestCase):
    def test_fixed_chunk_text_uses_overlap(self) -> None:
        chunks = fixed_chunk_text("abcdefghij", chunk_size=5, chunk_overlap=2)
        self.assertEqual(chunks, ["abcde", "defgh", "ghij"])

    def test_chunk_documents_adds_source_metadata(self) -> None:
        document = KnowledgeDocument(
            page_content="Section one.\n\nSection two.",
            metadata={
                "file_name": "sample.md",
                "source_file": "sample.md",
                "relative_path": "nested/sample.md",
                "source_path": "knowledge_base/nested/sample.md",
            },
        )

        chunks = chunk_documents([document], strategy="recursive", chunk_size=12, chunk_overlap=0)

        self.assertGreaterEqual(len(chunks), 2)
        self.assertEqual(chunks[0].metadata["chunk_strategy"], "recursive")
        self.assertEqual(chunks[0].metadata["chunk_id"], "nested/sample.md::recursive::0")
        self.assertEqual(chunks[0].metadata["file_name"], "sample.md")

    def test_recursive_chunk_text_keeps_small_text_as_one_chunk(self) -> None:
        self.assertEqual(
            recursive_chunk_text("small text", chunk_size=20, chunk_overlap=0),
            ["small text"],
        )


if __name__ == "__main__":
    unittest.main()
