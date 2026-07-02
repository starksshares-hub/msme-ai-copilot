import json  # for parsing JSON data
import logging  # for logging errors and information
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


def extract_invoice_data(invoice_text: str) -> InvoiceSchema | None:
    """
    Takes raw invoice text and extracts structured invoice data using Ollama.
    """

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
        response = ollama.chat(
            model="llama3.2",
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
                "temperature": 0
            }
        )

        raw_output = response["message"]["content"]

        # Reject invalid JSON
        try:
            parsed_json = json.loads(raw_output)
        except json.JSONDecodeError:
            logging.error("Invalid JSON returned by LLM: %s", raw_output)
            return None

        # Validate JSON with schema
        try:
            invoice = InvoiceSchema.model_validate(parsed_json)
        except ValidationError as e:
            logging.error("Schema validation failed: %s | Output: %s", e, parsed_json)
            return None

        return invoice

    except Exception as e:
        logging.exception("Invoice extraction failed: %s", e)
        return None