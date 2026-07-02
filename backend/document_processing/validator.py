from datetime import datetime
from typing import Any

from backend.document_processing.schema import REQUIRED_FIELDS


DATE_FIELDS = ["invoice_date", "due_date"]
MONEY_FIELDS = ["subtotal", "tax", "total_amount"]
TOLERANCE = 0.01


def add_error(errors: list[dict], field: str, message: str) -> None:
    errors.append(
        {
            "field": field,
            "error": message,
        }
    )


def is_blank(value: Any) -> bool:
    return value is None or str(value).strip() == ""


def is_valid_date(value: str) -> bool:
    """
    Accept common invoice date formats from extracted documents.
    """

    if is_blank(value):
        return False

    formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%d %b %Y",
        "%d %B %Y",
    ]

    for date_format in formats:
        try:
            datetime.strptime(str(value).strip(), date_format)
            return True
        except ValueError:
            continue

    return False


def validate_number(
    invoice_data: dict,
    field: str,
    errors: list[dict],
    allow_zero: bool = True,
) -> None:
    value = invoice_data.get(field, 0)

    try:
        number = float(value)
    except (TypeError, ValueError):
        add_error(errors, field, f"{field} must be a number")
        return

    if number < 0:
        add_error(errors, field, f"{field} cannot be negative")

    if not allow_zero and number == 0:
        add_error(errors, field, f"{field} must be greater than 0")


def validate_line_items(invoice_data: dict, errors: list[dict]) -> None:
    line_items = invoice_data.get("line_items", [])

    if line_items is None:
        return

    if not isinstance(line_items, list):
        add_error(errors, "line_items", "line_items must be a list")
        return

    for index, item in enumerate(line_items):
        if not isinstance(item, dict):
            add_error(errors, f"line_items[{index}]", "line item must be an object")
            continue

        for field in ["quantity", "unit_price", "total_price"]:
            try:
                value = float(item.get(field, 0))
            except (TypeError, ValueError):
                add_error(
                    errors,
                    f"line_items[{index}].{field}",
                    f"{field} must be a number",
                )
                continue

            if value < 0:
                add_error(
                    errors,
                    f"line_items[{index}].{field}",
                    f"{field} cannot be negative",
                )


def validate_invoice(invoice_data: dict) -> list[dict]:
    """
    Validate extracted invoice data before the processor returns it.
    """

    errors: list[dict] = []

    if not isinstance(invoice_data, dict):
        return [
            {
                "field": "invoice",
                "error": "Invoice data must be a dictionary",
            }
        ]

    for field in REQUIRED_FIELDS:
        if is_blank(invoice_data.get(field)):
            add_error(errors, field, f"{field} is required")

    for field in DATE_FIELDS:
        value = invoice_data.get(field, "")
        if value and not is_valid_date(value):
            add_error(errors, field, f"{field} has an invalid date format")

    for field in MONEY_FIELDS:
        validate_number(
            invoice_data=invoice_data,
            field=field,
            errors=errors,
            allow_zero=field != "total_amount",
        )

    confidence_score = invoice_data.get("confidence_score", 0)
    try:
        confidence = float(confidence_score)
        if confidence < 0 or confidence > 1:
            add_error(errors, "confidence_score", "confidence_score must be between 0 and 1")
    except (TypeError, ValueError):
        add_error(errors, "confidence_score", "confidence_score must be a number")

    validate_line_items(invoice_data, errors)

    try:
        subtotal = float(invoice_data.get("subtotal", 0) or 0)
        tax = float(invoice_data.get("tax", 0) or 0)
        total_amount = float(invoice_data.get("total_amount", 0) or 0)
    except (TypeError, ValueError):
        return errors

    if subtotal > 0 and total_amount > 0:
        expected_total = subtotal + tax
        if abs(expected_total - total_amount) > TOLERANCE:
            add_error(
                errors,
                "total_amount",
                "total_amount should match subtotal plus tax",
            )

    return errors
