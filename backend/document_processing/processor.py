# huff finally we are heare... nowww

"""
processor.py

This file controls the full invoice processing pipeline.

Flow:
1. Read invoice file using parser.py
2. Extract invoice data using extractor.py
3. Validate extracted data using validator.py
4. Return a clean structured result

Run from project root:

python -m backend.document_processing.processor backend/document_processing/sample_documents/sample_invoice.txt

or for folder:

python -m backend.document_processing.processor backend/document_processing/sample_documents
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any


# These imports work when you run:
# python -m backend.document_processing.processor
try:
    from .parser import parse_document
    from .extractor import extract_invoice_data
    from .validator import validate_invoice
except ImportError:
    # Backup imports if you run processor.py directly as a script.
    project_root = Path(__file__).resolve().parents[2]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    from backend.document_processing.parser import parse_document
    from backend.document_processing.extractor import extract_invoice_data
    from backend.document_processing.validator import validate_invoice


logger = logging.getLogger(__name__)


SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".markdown"}


def create_result(
    file_path: str,
    success: bool = False,
    data: dict | None = None,
    validation_errors: list | None = None,
    error: str = "",
) -> dict:
    """
    Create a standard response format for every processed invoice.
    """

    return {
        "success": success,
        "file_path": file_path,
        "data": data or {},
        "validation_errors": validation_errors or [],
        "error": error,
    }


def normalize_extracted_data(invoice_data: Any) -> dict:
    """
    Make sure extractor output becomes a normal Python dictionary.

    Extractor should ideally return dict.
    But sometimes it may return:
    - Pydantic model
    - JSON string
    - None
    """

    if invoice_data is None:
        return {}

    if isinstance(invoice_data, dict):
        return invoice_data

    # If extractor returns Pydantic model
    if hasattr(invoice_data, "model_dump"):
        return invoice_data.model_dump()

    # If extractor returns JSON string
    if isinstance(invoice_data, str):
        try:
            return json.loads(invoice_data)
        except json.JSONDecodeError:
            raise ValueError("Extractor returned invalid JSON string")

    raise TypeError(f"Unsupported extractor output type: {type(invoice_data)}")


def check_duplicate_invoice_number(
    invoice_data: dict,
    seen_invoice_numbers: set[str] | None,
) -> list[dict]:
    """
    Check duplicate invoice numbers during folder processing.

    Why here?
    Because duplicate checking needs memory of previous invoices.
    A single invoice alone cannot know if it is duplicate.
    """

    errors = []

    if seen_invoice_numbers is None:
        return errors

    invoice_number = str(invoice_data.get("invoice_number", "")).strip()

    if not invoice_number:
        return errors

    if invoice_number in seen_invoice_numbers:
        errors.append(
            {
                "field": "invoice_number",
                "error": f"Duplicate invoice number found: {invoice_number}",
            }
        )
    else:
        seen_invoice_numbers.add(invoice_number)

    return errors


def process_invoice(
    file_path: str,
    seen_invoice_numbers: set[str] | None = None,
) -> dict:
    """
    Process one invoice file.

    Steps:
    1. Check file exists
    2. Check file type is supported
    3. Parse text from file
    4. Extract invoice data using AI
    5. Validate invoice data
    6. Return final structured result
    """

    try:
        path = Path(file_path)

        if not path.exists():
            return create_result(
                file_path=file_path,
                error="File does not exist",
            )

        if not path.is_file():
            return create_result(
                file_path=file_path,
                error="Path is not a file",
            )

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return create_result(
                file_path=file_path,
                error=f"Unsupported file type: {path.suffix}",
            )

        logger.info("Parsing document: %s", file_path)

        document_text = parse_document(str(path))

        if not document_text or not document_text.strip():
            return create_result(
                file_path=file_path,
                error="No text extracted from document",
            )

        logger.info("Extracting invoice data: %s", file_path)

        raw_invoice_data = extract_invoice_data(document_text)
        invoice_data = normalize_extracted_data(raw_invoice_data)

        if not invoice_data:
            return create_result(
                file_path=file_path,
                error="Extractor returned empty invoice data",
            )

        logger.info("Validating invoice data: %s", file_path)

        validation_errors = validate_invoice(invoice_data)

        duplicate_errors = check_duplicate_invoice_number(
            invoice_data=invoice_data,
            seen_invoice_numbers=seen_invoice_numbers,
        )

        validation_errors.extend(duplicate_errors)

        success = len(validation_errors) == 0

        return create_result(
            file_path=str(path),
            success=success,
            data=invoice_data,
            validation_errors=validation_errors,
            error="",
        )

    except Exception as e:
        logger.exception("Invoice processing failed for file: %s", file_path)

        return create_result(
            file_path=file_path,
            success=False,
            data={},
            validation_errors=[],
            error=str(e),
        )


def process_invoice_folder(folder_path: str) -> list[dict]:
    """
    Process all supported invoice files inside a folder.

    Supported:
    - .pdf
    - .txt
    - .md
    - .markdown
    """

    folder = Path(folder_path)

    if not folder.exists():
        return [
            create_result(
                file_path=folder_path,
                error="Folder does not exist",
            )
        ]

    if not folder.is_dir():
        return [
            create_result(
                file_path=folder_path,
                error="Path is not a folder",
            )
        ]

    invoice_files = [
        file
        for file in folder.rglob("*")
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    if not invoice_files:
        return [
            create_result(
                file_path=folder_path,
                error="No supported invoice files found in folder",
            )
        ]

    results = []
    seen_invoice_numbers: set[str] = set()

    for invoice_file in invoice_files:
        result = process_invoice(
            file_path=str(invoice_file),
            seen_invoice_numbers=seen_invoice_numbers,
        )

        results.append(result)

    return results


def print_result(result: dict | list[dict]) -> None:
    """
    Pretty print result as JSON.
    """

    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="Process invoice file or folder"
    )

    parser.add_argument(
        "path",
        help="Path to invoice file or folder",
    )

    args = parser.parse_args()

    input_path = Path(args.path)

    if input_path.is_dir():
        output = process_invoice_folder(str(input_path))
    else:
        output = process_invoice(str(input_path))

    print_result(output)
