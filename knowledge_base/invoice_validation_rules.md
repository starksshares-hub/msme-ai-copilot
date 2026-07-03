# Invoice Validation Rules

## Purpose

Invoice validation means checking whether an invoice is complete, correct, and safe to record before making payment or entering it into accounting records.

For MSMEs, invoice validation helps prevent:

* Wrong payments
* Duplicate payments
* Fake invoices
* GST calculation errors
* Missing vendor details
* Cash flow mistakes
* Accounting mismatches

An invoice should not be approved only because it “looks correct.” Important fields, totals, dates, and vendor details should be checked properly.

---

## Basic Invoice Validation Checklist

A valid invoice should usually contain:

| Field                | Why It Matters                          |
| -------------------- | --------------------------------------- |
| Invoice number       | Helps uniquely identify the invoice     |
| Invoice date         | Shows when the invoice was issued       |
| Vendor name          | Identifies who issued the invoice       |
| Vendor address       | Helps confirm supplier identity         |
| Vendor GSTIN         | Required for GST-related verification   |
| Buyer name           | Shows who the invoice is issued to      |
| Buyer GSTIN          | Needed for B2B GST invoices             |
| Item description     | Explains what was sold or supplied      |
| Quantity             | Shows number of goods or units supplied |
| Rate                 | Price per unit                          |
| Subtotal             | Total before tax                        |
| Tax rate             | GST percentage applied                  |
| Tax amount           | GST amount charged                      |
| Total amount         | Final payable amount                    |
| Payment terms        | Due date or credit period               |
| Bank/payment details | Used for making payment                 |

---

## Rule 1: Missing Invoice Number

### Problem

An invoice number is missing or blank.

### Why It Is Risky

The invoice number is one of the most important identifiers of an invoice. Without it, the invoice becomes difficult to track, verify, and match with payments.

### Example

Invalid invoice:

```text
Invoice Number: 
Date: 10-Apr-2026
Vendor: Gupta Traders
Total: ₹25,000
```

### Validation Rule

```text
Invoice number must not be empty.
```

### RAG Answer Example

If an invoice does not have an invoice number, it should be flagged as incomplete. The business should ask the vendor to issue a corrected invoice with a proper invoice number.

---

## Rule 2: Duplicate Invoice Number

### Problem

The same invoice number appears more than once for the same vendor.

### Why It Is Risky

Duplicate invoice numbers may indicate:

* Duplicate payment attempt
* Same invoice uploaded twice
* Vendor billing mistake
* Possible fraud
* Accounting entry duplication

### Example

| Vendor        | Invoice Number |        Date |  Amount |
| ------------- | -------------- | ----------: | ------: |
| Gupta Traders | INV-105        | 05-Apr-2026 | ₹18,000 |
| Gupta Traders | INV-105        | 12-Apr-2026 | ₹18,000 |

### Validation Rule

```text
For the same vendor, the same invoice number should not appear more than once.
```

### RAG Answer Example

If two invoices from the same vendor have the same invoice number, the system should flag them as possible duplicates. The business should verify whether one invoice was uploaded twice or whether the vendor made an error.

---

## Rule 3: Missing Vendor Name

### Problem

The invoice does not clearly show the vendor or supplier name.

### Why It Is Risky

Without the vendor name, the business cannot confirm who issued the invoice or whom payment should be made to.

### Example

Invalid invoice:

```text
Vendor Name: 
Invoice Number: INV-210
Total: ₹42,000
```

### Validation Rule

```text
Vendor name must not be empty.
```

### RAG Answer Example

An invoice without a vendor name should not be approved. The business should ask for a corrected invoice with the supplier name clearly mentioned.

---

## Rule 4: Missing Vendor GSTIN

### Problem

The invoice does not contain the vendor GSTIN.

### Why It Is Risky

For GST invoices, the vendor GSTIN helps verify whether the supplier is registered under GST. Missing GSTIN can create problems while claiming input tax credit.

### Example

Invalid invoice:

```text
Vendor: Mehta Chemicals
GSTIN: 
Tax Amount: ₹9,000
Total: ₹59,000
```

### Validation Rule

```text
If GST is charged, vendor GSTIN should be present.
```

### RAG Answer Example

If GST is charged but the vendor GSTIN is missing, the invoice should be flagged. The buyer may face issues while claiming input tax credit.

---

## Rule 5: Invalid GSTIN Format

### Problem

The GSTIN is present but does not follow the correct format.

### Why It Is Risky

A wrong GSTIN may indicate typing errors, fake vendor details, or an invalid GST invoice.

### Basic GSTIN Format

A GSTIN usually has 15 characters.

Example format:

```text
27ABCDE1234F1Z5
```

### Validation Rule

```text
GSTIN should be 15 characters long and follow the expected GSTIN structure.
```

### RAG Answer Example

If the GSTIN format is invalid, the invoice should be flagged for review. The business should verify the GSTIN before recording GST credit.

---

## Rule 6: Missing Invoice Date

### Problem

The invoice date is missing.

### Why It Is Risky

Invoice date is required for:

* Accounting period
* GST reporting
* Payment due date calculation
* Aging analysis
* Cash flow planning

### Example

Invalid invoice:

```text
Invoice Number: INV-310
Date:
Vendor: Raj Steel Suppliers
Total: ₹75,000
```

### Validation Rule

```text
Invoice date must not be empty.
```

### RAG Answer Example

If the invoice date is missing, the invoice should not be processed until the vendor provides a corrected invoice.

---

## Rule 7: Invalid Date Format

### Problem

The invoice date is unclear, impossible, or written in an invalid format.

### Examples

Invalid dates:

```text
32-Apr-2026
2026-15-04
April 99, 2026
```

### Why It Is Risky

Wrong dates can create accounting errors and incorrect payment due dates.

### Validation Rule

```text
Invoice date must be a valid calendar date.
```

### RAG Answer Example

If the invoice date is invalid, the invoice should be flagged because it can affect payment planning and accounting records.

---

## Rule 8: Future Invoice Date

### Problem

The invoice date is later than the current date.

### Example

If today is 30-Apr-2026:

```text
Invoice Date: 15-May-2026
```

### Why It Is Risky

A future-dated invoice may be:

* Entered incorrectly
* Issued before actual supply
* Uploaded with the wrong date
* Not valid for current accounting records

### Validation Rule

```text
Invoice date should not be in the future unless specifically allowed.
```

### RAG Answer Example

A future-dated invoice should be reviewed before approval because it may create accounting and payment errors.

---

## Rule 9: Subtotal Plus Tax Does Not Equal Total

### Problem

The invoice total does not match subtotal plus tax.

### Correct Formula

```text
Subtotal + Tax = Total Amount
```

### Example

Invalid invoice:

```text
Subtotal: ₹10,000
GST: ₹1,800
Total: ₹12,500
```

Correct total should be:

```text
₹10,000 + ₹1,800 = ₹11,800
```

### Validation Rule

```text
Invoice total must equal subtotal plus tax, after considering rounding.
```

### RAG Answer Example

If subtotal plus tax does not equal the total amount, the invoice should be flagged for calculation mismatch.

---

## Rule 10: Line Item Total Mismatch

### Problem

The line item total does not match quantity multiplied by rate.

### Correct Formula

```text
Quantity × Rate = Line Item Amount
```

### Example

Invalid invoice:

| Item            | Quantity | Rate | Amount |
| --------------- | -------: | ---: | -----: |
| Packaging Boxes |      100 |  ₹50 | ₹6,000 |

Correct amount should be:

```text
100 × ₹50 = ₹5,000
```

### Validation Rule

```text
Each line item amount should equal quantity multiplied by rate.
```

### RAG Answer Example

If the line item amount is incorrect, the invoice should be flagged because the total payable amount may also be wrong.

---

## Rule 11: Tax Calculation Mismatch

### Problem

GST amount does not match the taxable value and GST rate.

### Correct Formula

```text
Taxable Value × GST Rate = GST Amount
```

### Example

Invalid invoice:

```text
Taxable Value: ₹50,000
GST Rate: 18%
GST Amount: ₹8,000
```

Correct GST should be:

```text
₹50,000 × 18% = ₹9,000
```

### Validation Rule

```text
GST amount should match taxable value multiplied by GST rate.
```

### RAG Answer Example

If GST amount is wrongly calculated, the invoice should be reviewed before recording it in accounts.

---

## Rule 12: Negative or Zero Invoice Amount

### Problem

The invoice total is zero or negative.

### Why It Is Risky

A normal sales or purchase invoice should usually have a positive payable amount. Zero or negative values may indicate wrong data entry or the wrong document type.

### Example

Invalid invoice:

```text
Total Amount: ₹0
```

### Validation Rule

```text
Invoice total should be greater than zero.
```

### RAG Answer Example

An invoice with zero or negative total should be flagged unless it is a special adjustment document, credit note, or correction entry.

---

## Rule 13: Missing Buyer Details

### Problem

The buyer name, buyer address, or buyer GSTIN is missing.

### Why It Is Risky

Buyer details confirm who the invoice is issued to. For B2B invoices, missing buyer details may create GST and accounting issues.

### Validation Rule

```text
Buyer details should be present, especially for B2B GST invoices.
```

### RAG Answer Example

If buyer details are missing, the invoice should be checked before approval because the invoice may not properly belong to the business.

---

## Rule 14: Due Date Before Invoice Date

### Problem

The payment due date is earlier than the invoice date.

### Example

Invalid invoice:

```text
Invoice Date: 10-Apr-2026
Due Date: 05-Apr-2026
```

### Why It Is Risky

This usually indicates a date entry error.

### Validation Rule

```text
Due date should be equal to or later than invoice date.
```

### RAG Answer Example

If the due date is before the invoice date, the invoice should be flagged because payment terms are incorrect.

---

## Rule 15: Missing Payment Terms

### Problem

The invoice does not mention payment terms or due date.

### Why It Is Risky

Missing payment terms can create confusion about when payment should be made.

### Examples of Payment Terms

```text
Due on receipt
Net 15
Net 30
Payment due by 30-Apr-2026
```

### Validation Rule

```text
Invoice should contain payment terms or a due date.
```

### RAG Answer Example

If payment terms are missing, the business may still record the invoice, but it should confirm the due date with the vendor for cash flow planning.

---

## Rule 16: Suspicious Vendor Bank Details

### Problem

The bank account details do not match the known vendor records.

### Why It Is Risky

Changed bank details can indicate:

* Vendor update
* Data entry mistake
* Email compromise
* Payment fraud attempt

### Validation Rule

```text
If vendor bank details are new or changed, verify before payment.
```

### RAG Answer Example

If bank details are different from previous records, the invoice should be held for verification before payment.

---

## Rule 17: Same Amount, Same Vendor, Close Dates

### Problem

Multiple invoices from the same vendor have the same amount and very close dates.

### Why It Is Risky

This may be a duplicate invoice even if invoice numbers are different.

### Example

| Vendor         | Invoice Number |        Date |  Amount |
| -------------- | -------------- | ----------: | ------: |
| City Logistics | CL-501         | 12-Apr-2026 | ₹14,000 |
| City Logistics | CL-502         | 13-Apr-2026 | ₹14,000 |

### Validation Rule

```text
Invoices from the same vendor with same amount and close dates should be reviewed.
```

### RAG Answer Example

This does not always prove fraud, but it should be checked to avoid duplicate payment.

---

## Rule 18: Missing Item Description

### Problem

The invoice does not clearly describe the goods or services supplied.

### Why It Is Risky

Without item descriptions, the buyer cannot confirm what was purchased.

### Invalid Example

```text
Item: Goods
Amount: ₹45,000
```

### Better Example

```text
Item: 500 corrugated packaging boxes
Amount: ₹45,000
```

### Validation Rule

```text
Each invoice line item should have a clear description.
```

### RAG Answer Example

If item descriptions are vague or missing, the invoice should be reviewed before approval.

---

## Rule 19: Missing Quantity or Rate

### Problem

The invoice has item names but does not show quantity or rate.

### Why It Is Risky

Without quantity and rate, the buyer cannot verify whether the amount charged is correct.

### Validation Rule

```text
For goods invoices, quantity and rate should be present.
```

### RAG Answer Example

If quantity or rate is missing, the invoice should be flagged because line item calculations cannot be verified.

---

## Rule 20: Rounding Difference Too High

### Problem

The invoice total has a large difference due to claimed rounding.

### Normal Rounding Example

```text
Calculated Total: ₹10,000.40
Rounded Total: ₹10,000
Difference: ₹0.40
```

### Suspicious Rounding Example

```text
Calculated Total: ₹10,000
Invoice Total: ₹10,250
Difference: ₹250
```

### Validation Rule

```text
Small rounding differences may be allowed, but large differences should be flagged.
```

### RAG Answer Example

If the rounding difference is unusually high, the invoice should be reviewed for calculation errors.

---

## Common Validation Status Labels

| Status               | Meaning                                   |
| -------------------- | ----------------------------------------- |
| Valid                | Invoice passed all major checks           |
| Incomplete           | Important fields are missing              |
| Calculation Error    | Amounts or tax values do not match        |
| Duplicate Risk       | Similar or same invoice already exists    |
| Vendor Review Needed | Vendor details are missing or suspicious  |
| Payment Hold         | Invoice should not be paid until verified |
| Rejected             | Invoice is invalid or unsafe to process   |

---

## Example Valid Invoice

```text
Invoice Number: INV-2026-041
Invoice Date: 10-Apr-2026
Vendor Name: Gupta Paper Traders
Vendor GSTIN: 27ABCDE1234F1Z5
Buyer Name: Sharma Packaging Works
Item: Kraft Paper Rolls
Quantity: 100
Rate: ₹1,000
Subtotal: ₹1,00,000
GST Rate: 18%
GST Amount: ₹18,000
Total Amount: ₹1,18,000
Payment Terms: Net 30
Due Date: 10-May-2026
```

### Why This Invoice Looks Valid

* Invoice number is present.
* Vendor name is present.
* GSTIN is present.
* Invoice date is valid.
* Quantity and rate are present.
* Subtotal is correct.
* GST calculation is correct.
* Total equals subtotal plus tax.
* Payment terms and due date are present.

---

## Example Invalid Invoice

```text
Invoice Number:
Invoice Date: 35-Apr-2026
Vendor Name:
Subtotal: ₹50,000
GST Amount: ₹9,000
Total Amount: ₹65,000
Payment Terms:
```

### Problems Found

| Issue                  | Reason                                          |
| ---------------------- | ----------------------------------------------- |
| Missing invoice number | Invoice cannot be uniquely tracked              |
| Invalid date           | 35-Apr-2026 is not a real date                  |
| Missing vendor name    | Supplier cannot be identified                   |
| Total mismatch         | ₹50,000 + ₹9,000 should be ₹59,000, not ₹65,000 |
| Missing payment terms  | Due date cannot be calculated                   |

### Suggested Status

```text
Status: Rejected or Payment Hold
Reason: Missing critical fields and calculation mismatch
```

---

## Priority Level of Validation Rules

| Priority | Rule Type                 | Action                       |
| -------- | ------------------------- | ---------------------------- |
| High     | Missing invoice number    | Hold invoice                 |
| High     | Missing vendor name       | Hold invoice                 |
| High     | Duplicate invoice number  | Review before payment        |
| High     | Total mismatch            | Review before approval       |
| High     | Invalid invoice date      | Ask for corrected invoice    |
| Medium   | Missing payment terms     | Confirm due date             |
| Medium   | Missing buyer details     | Review                       |
| Medium   | Suspicious bank details   | Verify vendor                |
| Low      | Small rounding difference | Allow if reasonable          |
| Low      | Minor spelling issue      | Correct in records if needed |

---

## Questions This File Can Answer

### What makes an invoice invalid?

An invoice may be invalid if it has missing invoice number, missing vendor name, invalid date, duplicate invoice number, wrong GST calculation, or total amount mismatch.

### What should be checked before paying an invoice?

Before paying an invoice, check invoice number, vendor name, GSTIN, invoice date, due date, line items, subtotal, tax amount, total amount, duplicate invoice risk, and vendor bank details.

### Why is duplicate invoice number risky?

A duplicate invoice number is risky because it may cause duplicate payment or indicate that the same invoice was uploaded more than once.

### What is a total mismatch in an invoice?

A total mismatch happens when subtotal plus tax does not equal the final invoice total.

### What should be done if invoice date is invalid?

The invoice should be flagged, and the vendor should be asked to provide a corrected invoice.

### Should an invoice be paid if vendor details are missing?

No. If vendor details are missing, the invoice should be held until the supplier identity is confirmed.

### Why should vendor bank details be checked?

Vendor bank details should be checked to avoid sending payment to the wrong account or falling for payment fraud.

---

## RAG Notes

This document helps answer questions about invoice validation, invoice errors, duplicate invoices, missing invoice fields, GST calculation mismatch, payment risk, fake invoice detection, and invoice approval rules.

Useful search terms for retrieval:

* invoice validation rules
* missing invoice number
* missing vendor name
* invalid invoice date
* duplicate invoice number
* subtotal tax total mismatch
* GST calculation error
* invoice total mismatch
* vendor GSTIN missing
* invalid GSTIN
* payment hold invoice
* duplicate invoice detection
* invoice approval checklist
* invoice error detection
* MSME invoice checking
* fake invoice prevention
