from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str = ""
    quantity: float = 0.0
    unit_price: float = 0.0
    total_price: float = 0.0


class InvoiceSchema(BaseModel):
    invoice_number: str = ""
    vendor_name: str = ""
    invoice_date: str = ""
    due_date: str = ""
    currency: str = ""

    subtotal: float = 0.0
    tax: float = 0.0
    total_amount: float = 0.0

    line_items: list[LineItem] = Field(default_factory=list) # this means that if no line items are provided, it will default to an empty list

    payment_terms: str = ""
    confidence_score: float = 0.0


REQUIRED_FIELDS = [
    "invoice_number",
    "vendor_name",
    "invoice_date",
    "total_amount",
]


def get_empty_invoice_schema() -> dict:
    return InvoiceSchema().model_dump()


if __name__ == "__main__":
    invoice = get_empty_invoice_schema()
    print(invoice)