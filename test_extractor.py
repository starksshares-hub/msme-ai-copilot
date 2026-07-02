from backend.document_processing.extractor import extract_invoice_data

sample_text = """
Invoice No: INV-101
Vendor: ABC Traders
Invoice Date: 2026-07-01
Due Date: 2026-07-10
Currency: INR

Item: Keyboard
Quantity: 2
Unit Price: 500
Total Price: 1000

Subtotal: 1000
Tax: 180
Total Amount: 1180
"""

result = extract_invoice_data(sample_text)

if result:
    print(result.model_dump_json(indent=4))
else:
    print("Extraction failed. Check logs/extractor.log")