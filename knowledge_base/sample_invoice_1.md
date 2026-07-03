# Sample Invoice 1: Valid GST Invoice Example

This is a sample invoice used for training an invoice extraction, invoice validation, and RAG-based MSME finance assistant. The invoice below represents a normal B2B GST invoice with clear supplier details, buyer details, GSTIN, invoice number, item details, tax calculation, payment terms, and bank details.

---

## Invoice Type

Tax Invoice

---

## Supplier Details

**Supplier Name:** ABC Office Supplies Pvt Ltd
**Trade Name:** ABC Office Mart
**Supplier GSTIN:** 27ABCDE1234F1Z5
**Supplier Address:**
Shop No. 12, Andheri Industrial Estate,
Andheri East, Mumbai, Maharashtra - 400069

**State:** Maharashtra
**State Code:** 27
**Email:** [accounts@abcofficemart.in](mailto:accounts@abcofficemart.in)
**Phone:** +91-9876543210

---

## Buyer Details

**Buyer Name:** Zenith Retail Solutions
**Buyer GSTIN:** 27ZYXWV9876L1Z2
**Buyer Address:**
Office No. 304, Business Square,
Bandra Kurla Complex, Mumbai, Maharashtra - 400051

**State:** Maharashtra
**State Code:** 27
**Email:** [finance@zenithretail.in](mailto:finance@zenithretail.in)

---

## Invoice Details

**Invoice Number:** INV-2025-26-001
**Invoice Date:** 15 April 2025
**Due Date:** 30 April 2025
**Payment Terms:** Payment due within 15 days
**Place of Supply:** Maharashtra
**Reverse Charge Applicable:** No
**Purchase Order Number:** PO-ZRS-2025-041

---

## Line Items

| Sr. No. | Item Description     | HSN Code | Quantity | Unit  | Rate per Unit | Taxable Value | GST Rate |
| ------: | -------------------- | -------: | -------: | ----- | ------------: | ------------: | -------: |
|       1 | A4 Copier Paper Ream |     4802 |       20 | Ream  |          ₹250 |        ₹5,000 |      18% |
|       2 | Ball Pens Pack       |     9608 |       10 | Pack  |          ₹150 |        ₹1,500 |      18% |
|       3 | Office Files         |     4820 |       25 | Piece |           ₹40 |        ₹1,000 |      18% |

---

## Tax Calculation

Since both supplier and buyer are located in Maharashtra, this is an intra-state supply. Therefore, CGST and SGST are charged.

| Description              | Amount |
| ------------------------ | -----: |
| Subtotal / Taxable Value | ₹7,500 |
| CGST @ 9%                |   ₹675 |
| SGST @ 9%                |   ₹675 |
| IGST                     |     ₹0 |
| Total GST                | ₹1,350 |
| Grand Total              | ₹8,850 |

---

## Amount in Words

Rupees Eight Thousand Eight Hundred Fifty Only

---

## Bank Details

**Account Holder Name:** ABC Office Supplies Pvt Ltd
**Bank Name:** HDFC Bank
**Account Number:** 123456789012
**IFSC Code:** HDFC0001234
**Branch:** Andheri East, Mumbai
**UPI ID:** abcofficesupplies@hdfcbank

---

## Declaration

We declare that this invoice shows the actual price of the goods described and that all particulars are true and correct.

---

## Authorized Signature

For ABC Office Supplies Pvt Ltd

Authorized Signatory

---

## Extracted JSON Example

```json
{
  "invoice_type": "Tax Invoice",
  "supplier_name": "ABC Office Supplies Pvt Ltd",
  "supplier_trade_name": "ABC Office Mart",
  "supplier_gstin": "27ABCDE1234F1Z5",
  "supplier_address": "Shop No. 12, Andheri Industrial Estate, Andheri East, Mumbai, Maharashtra - 400069",
  "supplier_state": "Maharashtra",
  "supplier_state_code": "27",
  "supplier_email": "accounts@abcofficemart.in",
  "supplier_phone": "+91-9876543210",
  "buyer_name": "Zenith Retail Solutions",
  "buyer_gstin": "27ZYXWV9876L1Z2",
  "buyer_address": "Office No. 304, Business Square, Bandra Kurla Complex, Mumbai, Maharashtra - 400051",
  "buyer_state": "Maharashtra",
  "buyer_state_code": "27",
  "buyer_email": "finance@zenithretail.in",
  "invoice_number": "INV-2025-26-001",
  "invoice_date": "2025-04-15",
  "due_date": "2025-04-30",
  "payment_terms": "Payment due within 15 days",
  "place_of_supply": "Maharashtra",
  "reverse_charge_applicable": false,
  "purchase_order_number": "PO-ZRS-2025-041",
  "line_items": [
    {
      "sr_no": 1,
      "description": "A4 Copier Paper Ream",
      "hsn_code": "4802",
      "quantity": 20,
      "unit": "Ream",
      "rate_per_unit": 250,
      "taxable_value": 5000,
      "gst_rate": 18
    },
    {
      "sr_no": 2,
      "description": "Ball Pens Pack",
      "hsn_code": "9608",
      "quantity": 10,
      "unit": "Pack",
      "rate_per_unit": 150,
      "taxable_value": 1500,
      "gst_rate": 18
    },
    {
      "sr_no": 3,
      "description": "Office Files",
      "hsn_code": "4820",
      "quantity": 25,
      "unit": "Piece",
      "rate_per_unit": 40,
      "taxable_value": 1000,
      "gst_rate": 18
    }
  ],
  "subtotal": 7500,
  "cgst": 675,
  "sgst": 675,
  "igst": 0,
  "total_gst": 1350,
  "grand_total": 8850,
  "amount_in_words": "Rupees Eight Thousand Eight Hundred Fifty Only",
  "bank_account_holder": "ABC Office Supplies Pvt Ltd",
  "bank_name": "HDFC Bank",
  "account_number": "123456789012",
  "ifsc_code": "HDFC0001234",
  "upi_id": "abcofficesupplies@hdfcbank"
}
```

---

## Validation Notes

This invoice is mostly valid because:

1. Supplier GSTIN is present.
2. Buyer GSTIN is present.
3. Invoice number is present and unique.
4. Invoice date and due date are clearly mentioned.
5. Supplier and buyer are in the same state.
6. CGST and SGST are charged correctly for intra-state supply.
7. IGST is not charged.
8. Line item totals are mathematically correct.
9. Subtotal matches the sum of taxable values.
10. GST calculation is correct.
11. Grand total matches subtotal plus GST.
12. Bank account holder name matches supplier name.
13. Payment terms are clear.
14. Purchase order number is mentioned.

---

## Calculation Check

```text
Item 1: 20 × ₹250 = ₹5,000
Item 2: 10 × ₹150 = ₹1,500
Item 3: 25 × ₹40 = ₹1,000

Subtotal = ₹5,000 + ₹1,500 + ₹1,000
Subtotal = ₹7,500

GST Rate = 18%
Total GST = ₹7,500 × 18%
Total GST = ₹1,350

CGST = ₹675
SGST = ₹675
IGST = ₹0

Grand Total = ₹7,500 + ₹1,350
Grand Total = ₹8,850
```

---

## RAG Questions This File Can Answer

### Question: Is this invoice valid?

Answer: Yes, this invoice appears valid because it contains supplier details, buyer details, GSTINs, invoice number, invoice date, line items, HSN codes, tax calculation, payment terms, and bank details.

### Question: Why are CGST and SGST charged?

Answer: CGST and SGST are charged because both supplier and buyer are located in Maharashtra. This makes it an intra-state transaction.

### Question: Why is IGST not charged?

Answer: IGST is not charged because the transaction is not inter-state. IGST usually applies when supplier and buyer are in different states.

### Question: What is the taxable value?

Answer: The taxable value is ₹7,500.

### Question: What is the total GST?

Answer: The total GST is ₹1,350, made up of ₹675 CGST and ₹675 SGST.

### Question: What is the grand total?

Answer: The grand total is ₹8,850.

### Question: Does the bank account look suspicious?

Answer: No. The bank account holder name is ABC Office Supplies Pvt Ltd, which matches the supplier name.

### Question: What should be extracted from this invoice?

Answer: The AI system should extract supplier name, supplier GSTIN, buyer name, buyer GSTIN, invoice number, invoice date, due date, line items, HSN codes, quantity, rate, taxable value, GST rate, CGST, SGST, IGST, grand total, payment terms, and bank details.

---

## Risk Score

**Risk Level:** Low Risk

**Reason:** The invoice contains all major required fields, totals are correct, GST treatment matches the supplier and buyer state, and bank details match the supplier name.

---

## Use in RAG System

This file should be used as a clean sample invoice. It helps the RAG assistant understand what a normal valid invoice looks like and how to answer invoice-related questions.

Good use cases:

```text
- Invoice field extraction
- GST tax calculation explanation
- Valid invoice example
- Intra-state GST example
- CGST and SGST example
- Invoice validation training
- Low-risk invoice example
```
