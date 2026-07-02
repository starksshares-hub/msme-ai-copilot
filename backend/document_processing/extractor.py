import json  # for parsing JSON data
import logging  # for logging errors and information
import os  # for reading environment variables
import re  # for extracting clear invoice fields from parsed text
from pathlib import Path  # for handling file paths

import ollama  # for interacting with the Ollama API
from pydantic import ValidationError  # for validating data models

from backend.document_processing.schema import InvoiceSchema


# Create logs folder if it does not exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


# Configure logging
logging.basicConfig(
    filename=LOG_DIR / "extractor.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")
OLLAMA_TIMEOUT_SECONDS = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "60"))
MAX_INVOICE_TEXT_CHARS = int(os.getenv("MAX_INVOICE_TEXT_CHARS", "8000"))

ollama_client = ollama.Client(timeout=OLLAMA_TIMEOUT_SECONDS)


def parse_amount(value: str) -> float:
    return float(value.replace(",", "").strip())


def first_match(pattern: str, text: str) -> str:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return ""

    return match.group(1).strip()


def extract_due_date(invoice_text: str) -> str:
    return first_match(
        r"(?:Due\s*date|Payment\s*due|Due\s*on)\s*:?\s*\n?\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4})",
        invoice_text,
    )


def extract_payment_terms(invoice_text: str) -> str:
    return first_match(
        r"(?:Payment\s*terms|Terms)\s*:?\s*\n?\s*([^\n]+)",
        invoice_text,
    )


def extract_line_items(invoice_text: str) -> list[dict]:
    """
    Extract rows from PDFs where invoice item columns become line-separated text.
    """

    items_section_match = re.search(
        r"ITEMS\s*(.*?)(?:SUMMARY|Total\s*\n)",
        invoice_text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not items_section_match:
        return []

    items_section = items_section_match.group(1)
    item_blocks = re.findall(
        r"(?:^|\n)\d+\.\s*\n(.*?)(?=\n\d+\.\s*\n|\Z)",
        items_section,
        flags=re.DOTALL,
    )

    line_items = []

    for block in item_blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]

        if len(lines) < 7:
            continue

        description_lines = lines[:-6]
        quantity_text = lines[-6]
        unit_price_text = lines[-4]
        total_price_text = lines[-3]

        try:
            line_items.append(
                {
                    "description": " ".join(description_lines),
                    "quantity": parse_amount(quantity_text),
                    "unit_price": parse_amount(unit_price_text),
                    "total_price": parse_amount(total_price_text),
                }
            )
        except ValueError:
            continue

    return line_items


def enrich_invoice_data(invoice_data: dict, invoice_text: str) -> dict:
    """
    Fix fields that are explicitly present in the parsed invoice text.
    """

    invoice_number = first_match(r"Invoice\s*no:\s*([^\n]+)", invoice_text)
    if invoice_number:
        invoice_data["invoice_number"] = invoice_number

    invoice_date = first_match(r"Date\s*of\s*issue:\s*\n?\s*([0-9]{1,2}[/-][0-9]{1,2}[/-][0-9]{2,4})", invoice_text)
    if invoice_date:
        invoice_data["invoice_date"] = invoice_date

    vendor_name = first_match(r"Seller:\s*\n\s*([^\n]+)", invoice_text)
    if vendor_name:
        invoice_data["vendor_name"] = vendor_name

    due_date = extract_due_date(invoice_text)
    if due_date:
        invoice_data["due_date"] = due_date

    payment_terms = extract_payment_terms(invoice_text)
    if payment_terms:
        invoice_data["payment_terms"] = payment_terms

    total_amounts = re.findall(r"INR\s*([0-9,]+(?:\.[0-9]+)?)", invoice_text)
    if len(total_amounts) >= 3:
        invoice_data["currency"] = "INR"
        invoice_data["subtotal"] = parse_amount(total_amounts[-3])
        invoice_data["tax"] = parse_amount(total_amounts[-2])
        invoice_data["total_amount"] = parse_amount(total_amounts[-1])

    line_items = extract_line_items(invoice_text)
    if line_items:
        invoice_data["line_items"] = line_items

    return invoice_data


def has_core_invoice_fields(invoice_data: dict) -> bool:
    return all(
        [
            invoice_data.get("invoice_number"),
            invoice_data.get("vendor_name"),
            invoice_data.get("invoice_date"),
            invoice_data.get("total_amount", 0) > 0,
        ]
    )


def extract_invoice_data(invoice_text: str) -> InvoiceSchema | None:
    """
    Takes raw invoice text and extracts structured invoice data using Ollama.
    """

    invoice_text = invoice_text[:MAX_INVOICE_TEXT_CHARS]
    parsed_invoice_data = enrich_invoice_data({}, invoice_text)

    if has_core_invoice_fields(parsed_invoice_data):
        parsed_invoice_data.setdefault("confidence_score", 0.95)
        return InvoiceSchema.model_validate(parsed_invoice_data)

    prompt = f"""
You are an invoice data extraction system.

Extract invoice information from the invoice text below.

Rules:
- Return ONLY valid JSON.
- Do not write explanation.
- Do not use markdown.
- If a field is missing, use:
  - "" for text fields
  - 0 for number fields
  - [] for list fields
- Dates should be strings.
- confidence_score should be between 0 and 1.

Invoice text:
{invoice_text}
"""

    try:
        response = ollama_client.chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You extract invoice data and return only valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            format=InvoiceSchema.model_json_schema(),
            options={
                "temperature": 0,
                "num_predict": 1000,
            }
        )

        raw_output = response["message"]["content"]

        # Reject invalid JSON
        try:
            parsed_json = json.loads(raw_output)
        except json.JSONDecodeError:
            logging.error("Invalid JSON returned by LLM: %s", raw_output)
            raise ValueError("Invalid JSON returned by LLM") from None

        # Validate JSON with schema
        try:
            enriched_json = enrich_invoice_data(parsed_json, invoice_text)
            invoice = InvoiceSchema.model_validate(enriched_json)
        except ValidationError as e:
            logging.error("Schema validation failed: %s | Output: %s", e, parsed_json)
            raise ValueError(f"Schema validation failed: {e}") from e

        return invoice

    except Exception as e:
        logging.exception("Invoice extraction failed: %s", e)
        raise RuntimeError(f"Invoice extraction failed using Ollama model '{OLLAMA_MODEL}': {e}") from e
