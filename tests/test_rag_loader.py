import tempfile
import unittest
from pathlib import Path

from backend.rag.loader import load_documents


class RagLoaderTests(unittest.TestCase):
    def test_load_documents_reads_nested_markdown_with_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            knowledge_base = Path(temp_dir) / "knowledge_base"
            nested_folder = knowledge_base / "gst"
            nested_folder.mkdir(parents=True)

            (knowledge_base / "invoice.md").write_text("Invoice guide", encoding="utf-8")
            (nested_folder / "returns.md").write_text("GST returns", encoding="utf-8")
            (nested_folder / "notes.txt").write_text("Skip me", encoding="utf-8")

            documents = load_documents(knowledge_base)
            by_relative_path = {
                document.metadata["relative_path"]: document
                for document in documents
            }

            self.assertEqual(set(by_relative_path), {"invoice.md", "gst/returns.md"})
            self.assertEqual(
                by_relative_path["invoice.md"].metadata["file_name"],
                "invoice.md",
            )
            self.assertEqual(
                by_relative_path["gst/returns.md"].metadata["file_name"],
                "returns.md",
            )
            self.assertEqual(
                by_relative_path["gst/returns.md"].page_content,
                "GST returns",
            )


if __name__ == "__main__":
    unittest.main()
