from pathlib import Path
import fitz  # PyMuPDF


def extract_text_from_pdf(file_path: str) -> str: # (file_path: str) -> str means the function takes a string as input and returns a string as output
    """
    Extract text from a PDF file.
    OCR/image-based PDFs are not supported yet.
    """
    text = ""

    with fitz.open(file_path) as document:
        for page in document:
            text += page.get_text() # += means append the text from each page to the overall text variable

    return text.strip() # strip means remove leading and trailing whitespace, including newlines


def extract_text_from_txt(file_path: str) -> str:
    """
    Extract text from a TXT file.
    """
    return Path(file_path).read_text(encoding="utf-8").strip() # this encoding ensures that the text is read correctly, especially for non-ASCII characters


def extract_text_from_markdown(file_path: str) -> str:
    """
    Extract text from a Markdown file.
    For now, we treat Markdown like normal text.
    """
    return Path(file_path).read_text(encoding="utf-8").strip()


def parse_document(file_path: str) -> str:
    """
    Main parser function.

    It checks the file type and sends it to the correct extractor.
    Supports:
    - PDF
    - TXT
    - Markdown
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    file_extension = path.suffix.lower() # get the file extension and convert it to lowercase for consistency suffix means the part of the filename after the last dot, including the dot itself (e.g., ".pdf", ".txt", ".md")

    if file_extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif file_extension == ".txt":
        return extract_text_from_txt(file_path)

    elif file_extension == ".md":
        return extract_text_from_markdown(file_path)

    else:
        raise ValueError(f"Unsupported file type: {file_extension}")


if __name__ == "__main__":
    sample_path = "backend/document_processing/sample_documents/invoice_51109328.pdf"

    print("Extracting text from document...")
    extracted_text = parse_document(sample_path)

    print("\nExtracted Text:")
    print(extracted_text)