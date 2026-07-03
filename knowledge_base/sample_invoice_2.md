# Sample Invoice 2: Suspicious / Fake Invoice Example

This is a sample suspicious invoice used for training an invoice extraction, invoice validation, fraud detection, and RAG-based MSME finance assistant.

This invoice intentionally contains multiple red flags such as wrong GSTIN format, missing invoice number, mismatched totals, suspicious vendor details, changed bank account, unclear line items, and GST calculation errors.

---

## Invoice Type

Tax Invoice

---

## Supplier Details

**Supplier Name:** QuickTech Business Solutions
**Trade Name:** QuickTech Services
**Supplier GSTIN:** 27QTECH12345Z
**Supplier Address:**
Near Main Road, Market Area,
Mumbai, Maharashtra

**State:** Maharashtra
**State Code:** 27
**Email:** [quicktechbilling@gmail.com](mailto:quicktechbilling@gmail.com)
**Phone:** +91-9999999999

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

**Invoice Number:** Missing
**Invoice Date:** 20 April 2025
**Due Date:** 21 April 2025
**Payment Terms:** Urgent payment required within 24 hours
**Place of Supply:** Maharashtra
**Reverse Charge Applicable:** Not mentioned
**Purchase Order Number:** Not mentioned

---

## Line Items

| Sr. No. | Item Description         | HSN/SAC Code | Quantity | Unit    | Rate per Unit | Taxable Value | GST Rate |
| ------: | ------------------------ | -----------: | -------: | ------- | ------------: | ------------: | -------: |
|       1 | Business service charges |      Missing |        1 | Service |       ₹40,000 |       ₹40,000 |      18% |
|       2 | Extra processing fees    |      Missing |        1 | Service |       ₹10,000 |       ₹10,000 |      18% |
|       3 | Miscellaneous charges    |      Missing |        1 | Service |        ₹5,000 |        ₹5,000 |      18% |

---

## Tax Calculation Shown on Invoice

The invoice claims that both supplier and buyer are located in Maharashtra. For an intra-state supply, CGST and SGST should normally be charged.

However, this invoice incorrectly shows IGST.

| Description              |  Amount |
| ------------------------ | ------: |
| Subtotal / Taxable Value | ₹55,000 |
| CGST                     |      ₹0 |
| SGST                     |      ₹0 |
| IGST @ 18%               | ₹12,500 |
| Total GST                | ₹12,500 |
| Grand Total              | ₹70,000 |

---

## Correct Calculation

The shown calculation is wrong.

```text id="2qzrie"
Subtotal = ₹40,000 + ₹10,000 + ₹5,000
Subtotal = ₹55,000

Correct GST @ 18% = ₹55,000 × 18%
Correct GST = ₹9,900

Since supplier and buyer are both in Maharashtra:
CGST @ 9% = ₹4,950
SGST @ 9% = ₹4,950
IGST = ₹0

Correct Grand Total = ₹55,000 + ₹9,900
Correct Grand Total = ₹64,900
```

The invoice shows grand total as ₹70,000, which does not match the correct calculation.

---

## Amount in Words

Rupees Seventy Five Thousand Only

---

## Bank Details

**Account Holder Name:** Rajesh Kumar
**Bank Name:** ICICI Bank
**Account Number:** 987654321000
**IFSC Code:** ICIC0004567
**Branch:** Thane
**UPI ID:** rajeshpay@upi

---

## Declaration

Payment must be made urgently. Delay may result in cancellation of service.

---

## Authorized Signature

For QuickTech Business Solutions

Authorized Signatory

---

## Extracted JSON Example

```json id="8xtl4v"
{
  "invoice_type": "Tax Invoice",
  "supplier_name": "QuickTech Business Solutions",
  "supplier_trade_name": "QuickTech Services",
  "supplier_gstin": "27QTECH12345Z",
  "supplier_address": "Near Main Road, Market Area, Mumbai, Maharashtra",
  "supplier_state": "Maharashtra",
  "supplier_state_code": "27",
  "supplier_email": "quicktechbilling@gmail.com",
  "supplier_phone": "+91-9999999999",
  "buyer_name": "Zenith Retail Solutions",
  "buyer_gstin": "27ZYXWV9876L1Z2",
  "buyer_address": "Office No. 304, Business Square, Bandra Kurla Complex, Mumbai, Maharashtra - 400051",
  "buyer_state": "Maharashtra",
  "buyer_state_code": "27",
  "buyer_email": "finance@zenithretail.in",
  "invoice_number": null,
  "invoice_date": "2025-04-20",
  "due_date": "2025-04-21",
  "payment_terms": "Urgent payment required within 24 hours",
  "place_of_supply": "Maharashtra",
  "reverse_charge_applicable": null,
  "purchase_order_number": null,
  "line_items": [
    {
      "sr_no": 1,
      "description": "Business service charges",
      "hsn_sac_code": null,
      "quantity": 1,
      "unit": "Service",
      "rate_per_unit": 40000,
      "taxable_value": 40000,
      "gst_rate": 18
    },
    {
      "sr_no": 2,
      "description": "Extra processing fees",
      "hsn_sac_code": null,
      "quantity": 1,
      "unit": "Service",
      "rate_per_unit": 10000,
      "taxable_value": 10000,
      "gst_rate": 18
    },
    {
      "sr_no": 3,
      "description": "Miscellaneous charges",
      "hsn_sac_code": null,
      "quantity": 1,
      "unit": "Service",
      "rate_per_unit": 5000,
      "taxable_value": 5000,
      "gst_rate": 18
    }
  ],
  "subtotal": 55000,
  "cgst": 0,
  "sgst": 0,
  "igst": 12500,
  "total_gst": 12500,
  "grand_total": 70000,
  "amount_in_words": "Rupees Seventy Five Thousand Only",
  "bank_account_holder": "Rajesh Kumar",
  "bank_name": "ICICI Bank",
  "account_number": "987654321000",
  "ifsc_code": "ICIC0004567",
  "upi_id": "rajeshpay@upi"
}
```

---

## Validation Result

This invoice should be treated as suspicious.

**Risk Level:** High Risk

**Recommended Action:** Do not approve payment until manual verification is completed.

---

## Red Flags Found

### 1. Invalid GSTIN Format

The supplier GSTIN is:

```text id="m1j1a8"
27QTECH12345Z
```

This GSTIN has only 13 characters. A normal GSTIN should have 15 characters.

### 2. Missing Invoice Number

The invoice number is missing. This is a serious issue because invoices should have a unique invoice number for tracking, accounting, GST records, and duplicate invoice detection.

### 3. Missing Purchase Order Number

The invoice does not mention any purchase order number. For a business invoice, especially a service invoice, it should usually be connected to an approved purchase order, contract, or service agreement.

### 4. Vague Line Items

The line items are unclear:

```text id="40m50x"
Business service charges
Extra processing fees
Miscellaneous charges
```

These descriptions are too vague. They do not explain what service was provided, when it was provided, or what deliverable was completed.

### 5. Missing HSN/SAC Codes

All line items have missing HSN/SAC codes. For service invoices, SAC codes are commonly expected for proper GST classification.

### 6. Wrong GST Type

Supplier and buyer are both located in Maharashtra. This is an intra-state transaction.

The invoice should normally charge:

```text id="mhmfa2"
CGST + SGST
```

But the invoice charges:

```text id="pw9db4"
IGST
```

This is a GST treatment mismatch.

### 7. GST Amount Is Wrong

The taxable value is ₹55,000 and GST rate is 18%.

Correct GST should be:

```text id="8ad9y3"
₹55,000 × 18% = ₹9,900
```

But the invoice shows GST as ₹12,500.

### 8. Grand Total Is Wrong

Correct grand total should be:

```text id="8sy9cq"
₹55,000 + ₹9,900 = ₹64,900
```

But the invoice shows:

```text id="n4xx3g"
₹70,000
```

This is a mismatch of ₹5,100.

### 9. Amount in Words Does Not Match Grand Total

The invoice shows grand total as ₹70,000, but amount in words says:

```text id="0bd8h3"
Rupees Seventy Five Thousand Only
```

This means the amount in words and amount in numbers do not match.

### 10. Suspicious Bank Account Holder

The supplier name is:

```text id="t63rng"
QuickTech Business Solutions
```

But the bank account holder is:

```text id="gym2rn"
Rajesh Kumar
```

This is suspicious because payment is being requested to a personal account instead of a business account.

### 11. Personal UPI ID

The UPI ID is:

```text id="blfeqd"
rajeshpay@upi
```

This looks like a personal UPI ID instead of a business UPI ID.

### 12. Urgent Payment Pressure

The invoice says payment is required within 24 hours. Urgency alone does not prove fraud, but it is a common warning sign when combined with changed bank details, personal account, missing invoice number, and mismatched totals.

### 13. Incomplete Supplier Address

The supplier address is vague:

```text id="m5i15z"
Near Main Road, Market Area, Mumbai, Maharashtra
```

It does not include building number, street name, PIN code, or proper registered office details.

### 14. Free Email Address

The supplier uses:

```text id="mtqkjh"
quicktechbilling@gmail.com
```

A Gmail address is not automatically fake, especially for small businesses, but it should be verified for a high-value invoice.

### 15. Reverse Charge Not Mentioned

The reverse charge field is not mentioned. This may not always be mandatory for every invoice format, but missing tax-related fields increase review risk.

---

## Fraud Detection Rules Triggered

```text id="8qc6ko"
Rule 1: GSTIN length is not 15 characters → High risk.
Rule 2: Invoice number is missing → High risk.
Rule 3: Purchase order number is missing → Medium/high risk.
Rule 4: GST type is wrong for intra-state supply → High risk.
Rule 5: GST amount does not match taxable value × GST rate → High risk.
Rule 6: Grand total does not match subtotal + GST → High risk.
Rule 7: Amount in words does not match amount in numbers → High risk.
Rule 8: Bank account holder does not match supplier name → High risk.
Rule 9: UPI ID appears personal → Medium/high risk.
Rule 10: Line item descriptions are vague → Medium risk.
Rule 11: HSN/SAC codes are missing → Medium risk.
Rule 12: Supplier address is incomplete → Medium risk.
Rule 13: Payment terms create urgency pressure → Medium risk.
```

---

## RAG Questions This File Can Answer

### Question: Is this invoice valid?

Answer: No. This invoice appears suspicious because the GSTIN is invalid, invoice number is missing, GST calculation is wrong, IGST is charged incorrectly, totals do not match, and payment is requested to a personal bank account.

### Question: What is wrong with the GSTIN?

Answer: The supplier GSTIN has only 13 characters. A normal GSTIN should have 15 characters, so this should be flagged.

### Question: Why is IGST wrong here?

Answer: Supplier and buyer are both located in Maharashtra. Since this is an intra-state transaction, CGST and SGST should normally be charged instead of IGST.

### Question: What should the correct GST be?

Answer: The taxable value is ₹55,000 and the GST rate is 18%. Correct GST should be ₹9,900.

### Question: What should the correct grand total be?

Answer: Correct grand total should be ₹64,900, calculated as ₹55,000 taxable value plus ₹9,900 GST.

### Question: Why is the bank account suspicious?

Answer: The supplier name is QuickTech Business Solutions, but the bank account holder is Rajesh Kumar. This mismatch may indicate payment diversion or vendor impersonation.

### Question: Should this invoice be paid?

Answer: No. Payment should be blocked until the supplier GSTIN, invoice number, bank details, purchase order, service proof, and tax calculation are manually verified.

### Question: What are the biggest red flags in this invoice?

Answer: The biggest red flags are invalid GSTIN, missing invoice number, wrong GST type, wrong GST amount, mismatched grand total, amount in words mismatch, missing purchase order, vague service description, and personal bank account details.

---

## Manual Verification Checklist

Before approving this invoice, the finance team should verify:

```text id="tv7hqu"
1. Is QuickTech Business Solutions a real registered vendor?
2. Is the supplier GSTIN valid?
3. Does the GSTIN match the supplier name?
4. Why is the invoice number missing?
5. Is there an approved purchase order?
6. Were the services actually provided?
7. Is there a service completion report?
8. Why is IGST charged for same-state supply?
9. Why does GST calculation not match 18%?
10. Why does grand total not match subtotal plus GST?
11. Why does amount in words say ₹75,000 while total says ₹70,000?
12. Why is payment going to Rajesh Kumar?
13. Is Rajesh Kumar authorized by the supplier?
14. Has this bank account been approved in vendor master data?
15. Was the payment urgency confirmed through official vendor contact?
```

---

## Corrected Invoice Calculation Example

If this invoice were genuine and the supplier and buyer were both in Maharashtra, the corrected tax calculation would look like this:

| Description              |  Amount |
| ------------------------ | ------: |
| Subtotal / Taxable Value | ₹55,000 |
| CGST @ 9%                |  ₹4,950 |
| SGST @ 9%                |  ₹4,950 |
| IGST                     |      ₹0 |
| Total GST                |  ₹9,900 |
| Correct Grand Total      | ₹64,900 |

---

## Risk Score

```text id="6bxr0n"
Risk Level: High Risk
Payment Status: Hold
Manual Review Required: Yes
Suggested Action: Verify vendor, GSTIN, PO, service proof, and bank details before payment.
```

---

## Use in RAG System

This file should be used as a suspicious invoice example. It helps the RAG assistant understand how to detect fake invoices, explain red flags, and recommend safe payment actions.

Good use cases:

```text id="sd3x1z"
- Fake invoice detection
- GST mismatch example
- Invalid GSTIN example
- Missing invoice number example
- Wrong tax calculation example
- Suspicious bank account example
- Vendor impersonation example
- High-risk invoice example
- Invoice validation training
```

---

## Simple Summary

This invoice should be flagged because:

```text id="dg7qeo"
1. GSTIN is invalid.
2. Invoice number is missing.
3. Purchase order is missing.
4. GST calculation is wrong.
5. IGST is incorrectly charged.
6. Grand total does not match calculation.
7. Amount in words does not match amount in numbers.
8. Bank account holder does not match supplier name.
9. UPI ID looks personal.
10. Line items are vague.
```

The invoice should not be paid until it is manually verified.
