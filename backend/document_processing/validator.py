from datetime import datetime
from typing import Any

from backend.document_processing.schema import REQUIRED_FIELDS


DATE_FORMATS = [
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%Y/%m/%d",
    "%d %b %Y",
    "%d %B %Y",
]


def is_blank(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def parse_date(date_text: str) -> datetime | None:
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(str(date_text).strip(), date_format)
        except ValueError:
            continue

    return None


def add_error(errors: list[dict], field: str, message: str) -> None:
    errors.append(
        {
            "field": field,
            "error": message,
        }
    )


def validate_invoice(invoice: dict, existing_invoice_numbers: list | None = None) -> list[dict]:
    errors: list[dict] = []

    if existing_invoice_numbers is None:
        existing_invoice_numbers = []

    if not isinstance(invoice, dict):
        return [{"field": "invoice", "error": "Invoice data must be a dictionary"}]

    for field in REQUIRED_FIELDS:
        if is_blank(invoice.get(field)):
            add_error(errors, field, f"{field} is required")

    invoice_number = invoice.get("invoice_number")
    if invoice_number and invoice_number in existing_invoice_numbers:
        add_error(errors, "invoice_number", "Invoice number already exists")

    invoice_date = invoice.get("invoice_date", "")
    due_date = invoice.get("due_date", "")

    parsed_invoice_date = parse_date(invoice_date) if invoice_date else None
    parsed_due_date = parse_date(due_date) if due_date else None

    if invoice_date and parsed_invoice_date is None:
        add_error(errors, "invoice_date", "invoice_date has an invalid date format")

    if due_date and parsed_due_date is None:
        add_error(errors, "due_date", "due_date has an invalid date format")

    if parsed_invoice_date and parsed_due_date and parsed_due_date < parsed_invoice_date:
        add_error(errors, "due_date", "Due date cannot be before invoice date")

    for field in ["subtotal", "tax", "total_amount"]:
        value = invoice.get(field, 0)
        if not is_number(value):
            add_error(errors, field, f"{field} must be a number")
        elif value < 0:
            add_error(errors, field, f"{field} cannot be negative")

    subtotal = invoice.get("subtotal", 0)
    tax = invoice.get("tax", 0)
    total_amount = invoice.get("total_amount", 0)

    if is_number(subtotal) and is_number(tax) and is_number(total_amount):
        if total_amount <= 0:
            add_error(errors, "total_amount", "total_amount must be greater than 0")

        if abs((subtotal + tax) - total_amount) > 1:
            add_error(errors, "total_amount", "Total amount does not match subtotal plus tax")

    line_items = invoice.get("line_items", [])
    if not isinstance(line_items, list):
        add_error(errors, "line_items", "line_items must be a list")
    else:
        line_items_total = 0.0

        for index, item in enumerate(line_items):
            if not isinstance(item, dict):
                add_error(errors, f"line_items[{index}]", "Line item must be a dictionary")
                continue

            quantity = item.get("quantity", 0)
            unit_price = item.get("unit_price", 0)
            total_price = item.get("total_price", 0)

            for field, value in [
                ("quantity", quantity),
                ("unit_price", unit_price),
                ("total_price", total_price),
            ]:
                if not is_number(value):
                    add_error(errors, f"line_items[{index}].{field}", f"{field} must be a number")
                elif value < 0:
                    add_error(errors, f"line_items[{index}].{field}", f"{field} cannot be negative")

            if is_number(quantity) and is_number(unit_price) and is_number(total_price):
                if abs((quantity * unit_price) - total_price) > 1:
                    add_error(
                        errors,
                        f"line_items[{index}].total_price",
                        "Line item total_price does not match quantity times unit_price",
                    )
                line_items_total += total_price

        if line_items and is_number(subtotal) and abs(line_items_total - subtotal) > 1:
            add_error(errors, "subtotal", "Subtotal does not match total of line items")

    confidence_score = invoice.get("confidence_score", 0)
    if not is_number(confidence_score):
        add_error(errors, "confidence_score", "confidence_score must be a number")
    elif confidence_score < 0 or confidence_score > 1:
        add_error(errors, "confidence_score", "confidence_score must be between 0 and 1")

    return errors
