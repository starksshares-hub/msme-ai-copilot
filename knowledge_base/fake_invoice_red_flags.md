# Fake Invoice Red Flags for MSMEs

Fake invoice detection means checking whether an invoice is genuine, complete, mathematically correct, and connected to a real business transaction. For MSMEs, fake invoices can cause cash loss, wrong GST claims, duplicate payments, bad accounting records, and legal or tax problems.

A valid GST tax invoice should contain prescribed fields such as supplier details, recipient details, GSTIN, invoice number, date, HSN/SAC, description, quantity, taxable value, tax rate, tax amount, place of supply, and other required particulars under Rule 46 of the CGST Rules. For applicable e-invoices, the Invoice Registration Portal generates an Invoice Reference Number, digitally signed e-invoice, and QR code.

## 1. Wrong or Suspicious GSTIN

A GSTIN is a 15-character Goods and Services Tax Identification Number. It should match the supplier’s legal business name, trade name, state, and registration status.

### Red flags

* GSTIN is missing even though GST is charged.
* GSTIN has fewer or more than 15 characters.
* GSTIN format looks random or copied.
* Supplier GSTIN belongs to a different business.
* GSTIN state code does not match the supplier’s address.
* GSTIN is inactive, cancelled, or invalid.
* GSTIN belongs to a business in a completely unrelated industry.
* Invoice shows one GSTIN, but bank account or letterhead shows another entity.

### Example

A vendor from Maharashtra gives an invoice with a GSTIN starting with `07`, which belongs to Delhi. This does not automatically prove fraud, but it should be verified because the GSTIN state code and vendor address do not match.

### AI detection rule

Flag the invoice if:

* `GSTIN` is missing while `CGST`, `SGST`, `IGST`, or `GST` amount is present.
* GSTIN length is not 15.
* GSTIN state code does not match supplier address state.
* Supplier name and GSTIN-registered name do not match.

## 2. Missing or Invalid Invoice Number

Every proper invoice should have a unique invoice number. Missing or duplicated invoice numbers are major warning signs.

### Red flags

* Invoice number is missing.
* Invoice number is handwritten on a printed invoice.
* Same invoice number appears for two different invoices.
* Invoice number sequence looks broken or suspicious.
* Invoice number contains strange characters or inconsistent formatting.
* Vendor uses different invoice numbering styles every time without reason.
* Invoice number is reused after changing only the date or amount.

### Example

Invoice `INV-1024` appears twice: once for ₹18,000 and once for ₹42,000. This may indicate duplication, tampering, or poor vendor recordkeeping.

### AI detection rule

Flag the invoice if:

* `invoice_number` is empty.
* Same `vendor_name + invoice_number + financial_year` already exists.
* Same invoice number appears with different amount, date, or buyer.
* Invoice number format differs heavily from previous invoices from the same vendor.

## 3. Mismatched Totals

Fake or manipulated invoices often have calculation errors. Totals should match line items, tax amounts, discounts, and grand total.

### Red flags

* Line item total does not equal quantity × rate.
* Subtotal does not match sum of line items.
* GST amount is calculated on the wrong taxable value.
* CGST + SGST + IGST does not match total tax.
* Grand total does not equal taxable value + tax - discount.
* Amount in words does not match amount in numbers.
* Rounding difference is too large.
* Same item has different rates within the same invoice without explanation.

### Example

Line items total ₹50,000. GST at 18% should be ₹9,000. Grand total should be ₹59,000. If the invoice shows ₹62,000 without freight, extra charges, or explanation, it should be flagged.

### AI detection rule

Calculate:

```text
line_total = quantity × rate
subtotal = sum(line_total)
tax_total = CGST + SGST + IGST
grand_total = subtotal - discount + tax_total + other_charges
```

Flag the invoice if calculated grand total and invoice grand total differ beyond a small rounding tolerance.

## 4. Suspicious Vendor Details

A fake invoice may use incomplete, mismatched, or low-quality vendor information.

### Red flags

* Vendor name is missing.
* Vendor address is incomplete.
* Vendor address looks fake or too generic.
* Vendor phone number or email is missing.
* Email uses a suspicious free domain for a large supplier.
* Vendor name differs across invoice, GSTIN, bank account, and purchase order.
* Bank account holder name does not match vendor name.
* Vendor logo is blurry, stretched, or copied.
* Vendor has no website, business listing, or verifiable presence.
* Vendor asks for payment to a personal account instead of a business account.

### Example

Invoice says supplier is `ABC Steel Traders Pvt Ltd`, but payment account holder is `Ramesh Kumar`. This should be reviewed before payment.

### AI detection rule

Flag the invoice if:

* Vendor name is different from bank account holder name.
* Vendor GSTIN business name differs from invoice vendor name.
* Vendor address is missing or does not include city/state.
* Vendor details changed compared with previous invoices.

## 5. Duplicate Invoices

Duplicate invoices are common in payment fraud and accounting mistakes. Sometimes the same invoice is submitted twice with small changes.

### Red flags

* Same invoice number submitted more than once.
* Same vendor, same date, same amount, same buyer.
* Same PDF file uploaded with different filename.
* Same line items but slightly changed invoice number.
* Same invoice submitted by both vendor and employee.
* Credit note or revised invoice not linked properly.
* Old invoice resubmitted after several months.

### Example

A vendor submits `INV-889` for ₹24,500 in March. In April, another invoice `INV-889A` appears with the same amount and same items. This may be a duplicate disguised as a new bill.

### AI detection rule

Check similarity using:

```text
vendor_name
invoice_number
invoice_date
total_amount
GSTIN
line_items
bank_account
file_hash
```

Flag when two invoices are highly similar even if one field is slightly changed.

## 6. GST Tax Red Flags

GST-related mistakes can indicate fake billing, wrong classification, or careless accounting.

### Red flags

* GST charged by an unregistered supplier.
* CGST and SGST charged for inter-state supply instead of IGST.
* IGST charged for intra-state supply instead of CGST + SGST.
* GST rate seems wrong for the item or service.
* Taxable value is missing.
* HSN/SAC code is missing where required.
* GST amount does not match GST rate.
* Reverse charge field is missing where applicable.
* Place of supply is missing or inconsistent.

### Example

Supplier and buyer are both in Gujarat, but invoice charges IGST. This should be verified because intra-state supplies usually use CGST + SGST.

### AI detection rule

Flag if:

* Supplier state = buyer state and invoice has IGST instead of CGST + SGST.
* Supplier state ≠ buyer state and invoice has CGST + SGST instead of IGST.
* GST amount is not equal to taxable value × GST rate.
* HSN/SAC is missing for taxable goods/services.

## 7. E-Invoice Red Flags

For businesses covered under e-invoicing rules, the invoice should have proper e-invoice details such as IRN and QR code. The GST e-invoice portal states that the IRP generates the IRN, digitally signed e-invoice, and QR code.

### Red flags

* IRN is missing when e-invoicing is applicable.
* QR code is missing or unreadable.
* QR code data does not match invoice data.
* IRN belongs to a different invoice.
* E-invoice date and printed invoice date differ suspiciously.
* Invoice claims to be an e-invoice but has no digital signature/QR details.
* QR code appears pasted as an image and does not scan.

### AI detection rule

Flag if:

* `is_e_invoice_required = true` and `IRN` is missing.
* QR code exists but cannot be decoded.
* QR code invoice number, GSTIN, date, or amount differs from visible invoice.

## 8. Purchase Order and Delivery Mismatch

A real invoice should usually connect to a purchase order, delivery challan, goods receipt note, service completion proof, or contract.

### Red flags

* No purchase order reference.
* Invoice amount exceeds purchase order amount.
* Invoice items do not match purchase order items.
* Quantity billed is more than quantity received.
* Delivery challan is missing.
* Goods receipt note is missing.
* Service invoice has no work completion proof.
* Invoice date is before purchase order date.
* Invoice raised after vendor contract expired.

### Example

Purchase order approved 100 units, but invoice bills 140 units. Unless there is an approved amendment, this should be flagged.

### AI detection rule

Compare invoice with:

```text
purchase_order
goods_receipt_note
delivery_challan
contract
service_completion_report
```

Flag if invoice quantity, rate, item description, or total amount does not match approved documents.

## 9. Suspicious Dates

Invoice dates can reveal fake or backdated billing.

### Red flags

* Invoice date is in the future.
* Invoice date is before vendor onboarding date.
* Invoice date is before purchase order date.
* Due date is missing.
* Due date is unusually short or unusually long.
* Invoice submitted long after the invoice date.
* Multiple invoices created on the same date with non-sequential numbering.
* Invoice date falls on a holiday/weekend for a vendor that normally does not bill then.

### Example

A vendor onboarded on 10 June submits an invoice dated 2 June. This should be reviewed because the invoice predates the vendor relationship.

### AI detection rule

Flag if:

* `invoice_date > today`
* `invoice_date < vendor_onboarding_date`
* `invoice_date < purchase_order_date`
* `invoice_submission_date - invoice_date` is unusually high.

## 10. Bank Account and Payment Red Flags

Payment fraud often happens when invoice bank details are manipulated.

### Red flags

* Bank account holder name does not match vendor name.
* New bank account added without approval.
* Bank branch location does not match vendor location.
* Payment requested to personal account.
* Vendor asks for urgent payment to a different account.
* Bank details differ from previous invoices.
* UPI ID looks personal instead of business-related.
* Invoice says one bank account, email body says another.

### Example

Vendor’s previous invoices used `ABC Enterprises Current Account`, but the latest invoice asks payment to `abcowner@upi`. This should be verified manually.

### AI detection rule

Flag if:

* Bank account changed from previous vendor master data.
* Account holder name differs from vendor legal name.
* Payment details in invoice and email body do not match.
* New account is used for high-value invoice.

## 11. Document Formatting Red Flags

Fake invoices may look visually inconsistent or poorly edited.

### Red flags

* Fonts are inconsistent.
* Text alignment looks edited.
* Logo is blurry or pixelated.
* Tax amount appears pasted or overwritten.
* Invoice has spelling mistakes in legal fields.
* PDF metadata shows recent editing after invoice date.
* Invoice file name looks suspicious.
* Same template used by unrelated vendors.
* Different pages have different layouts.
* Signature appears copied from another document.

### Example

Invoice date is 15 April, but PDF metadata shows it was created on 25 May after the payment dispute started. This does not prove fraud, but it deserves review.

### AI detection rule

Flag if:

* OCR text and visible layout conflict.
* PDF metadata creation date is much later than invoice date.
* Signature image appears reused across multiple vendors.
* Invoice template matches unrelated vendors.

## 12. Suspicious Line Items

Line item details should be clear and business-relevant.

### Red flags

* Item description is vague, such as “services”, “material”, or “charges”.
* Quantity is missing.
* Unit rate is missing.
* HSN/SAC is missing.
* Same item appears multiple times without reason.
* Item is unrelated to buyer’s business.
* Price is much higher than past purchases.
* Round-number billing appears repeatedly.
* High-value invoice has no item-level details.

### Example

An invoice for ₹4,80,000 says only “consulting services” with no hours, deliverables, contract, or service period. This should be checked before payment.

### AI detection rule

Flag if:

* Description length is too short.
* Quantity or rate is missing.
* Line item price is much higher than vendor history.
* Item does not match purchase order category.

## 13. Common Fake Invoice Patterns

### Pattern 1: Fake GST invoice for ITC

A fake supplier issues an invoice without actual supply of goods or services. The buyer may wrongly claim Input Tax Credit.

Red flags:

* No actual goods received.
* No e-way bill or delivery proof.
* Supplier has suspicious GST registration.
* Invoice exists only for tax credit.

### Pattern 2: Duplicate payment fraud

The same invoice is submitted more than once with small changes.

Red flags:

* Same amount and date.
* Slightly changed invoice number.
* Same PDF with renamed file.
* Same vendor bank account.

### Pattern 3: Vendor impersonation

A fraudster sends an invoice pretending to be a real vendor.

Red flags:

* Email domain differs from usual vendor email.
* Bank details changed suddenly.
* Urgent payment request.
* Invoice template looks similar but not identical.

### Pattern 4: Inflated invoice

A real vendor submits an invoice with inflated quantity, rate, or tax.

Red flags:

* Quantity exceeds goods received.
* Rate exceeds purchase order.
* Extra charges not approved.
* GST calculated on inflated taxable value.

### Pattern 5: Shell vendor billing

A fake or related-party vendor is created only to raise invoices.

Red flags:

* Vendor has no real business activity.
* Same address used by many vendors.
* Same phone/email used across vendors.
* Bank account linked to employee or related party.

## 14. Risk Scoring System for AI/RAG Assistant

Use a risk score to classify invoices.

### Low risk

Invoice has all required fields, totals match, GSTIN looks valid, vendor is known, bank details match vendor master, and invoice matches purchase order.

### Medium risk

Invoice has small issues such as minor rounding difference, missing optional field, delayed submission, or first-time vendor requiring verification.

### High risk

Invoice has wrong GSTIN, missing invoice number, mismatched totals, unknown vendor, changed bank account, duplicate invoice number, or missing delivery proof.

### Critical risk

Invoice appears fake, duplicated, forged, or unrelated to any real supply. Payment should be blocked until manual review.

## 15. Suggested RAG Q&A Examples

### Question

How can I identify a fake invoice?

### Answer

Check the GSTIN, invoice number, vendor details, tax calculation, line item totals, bank account, purchase order match, and duplicate invoice history. A fake invoice often has missing GSTIN, invalid invoice number, mismatched totals, suspicious vendor details, or no proof of actual goods/services supplied.

### Question

What is the biggest red flag in an invoice?

### Answer

The biggest red flags are invalid GSTIN, duplicate invoice number, mismatched total amount, changed bank account, and invoice not matching purchase order or delivery records.

### Question

Can a wrong GSTIN mean the invoice is fake?

### Answer

A wrong GSTIN does not always prove fraud, but it is a serious red flag. The GSTIN should be verified against the supplier’s legal name, state, and registration status.

### Question

What should I do before paying a suspicious invoice?

### Answer

Do not pay immediately. Verify GSTIN, confirm vendor bank details, compare with purchase order, check goods receipt or service proof, recalculate totals, and ask the vendor for clarification.

### Question

How can duplicate invoices be detected?

### Answer

Compare invoice number, vendor name, GSTIN, date, total amount, line items, bank details, and file hash. Even if invoice numbers differ slightly, similar date, amount, and line items may indicate duplication.

## 16. Invoice Verification Checklist

Before approving an invoice, check:

```text
1. Is supplier name present?
2. Is supplier GSTIN present and valid?
3. Is buyer name present?
4. Is invoice number present and unique?
5. Is invoice date valid?
6. Are line items clear?
7. Are quantity and rate present?
8. Does subtotal match line items?
9. Is GST calculated correctly?
10. Does grand total match subtotal + tax - discount?
11. Does amount in words match amount in numbers?
12. Does invoice match purchase order?
13. Does invoice match goods receipt/service proof?
14. Are bank details same as vendor master?
15. Is this invoice a duplicate?
16. Is IRN/QR code present where e-invoice is applicable?
17. Are vendor email and domain trusted?
18. Is payment request normal, or unusually urgent?
```

## 17. Fields to Extract for Fake Invoice Detection

For an AI invoice checker, extract these fields:

```json
{
  "supplier_name": "",
  "supplier_gstin": "",
  "supplier_address": "",
  "buyer_name": "",
  "buyer_gstin": "",
  "invoice_number": "",
  "invoice_date": "",
  "purchase_order_number": "",
  "line_items": [
    {
      "description": "",
      "hsn_sac": "",
      "quantity": "",
      "unit": "",
      "rate": "",
      "taxable_value": "",
      "gst_rate": "",
      "tax_amount": "",
      "total": ""
    }
  ],
  "subtotal": "",
  "discount": "",
  "cgst": "",
  "sgst": "",
  "igst": "",
  "total_tax": "",
  "grand_total": "",
  "amount_in_words": "",
  "bank_account_holder": "",
  "bank_account_number": "",
  "ifsc": "",
  "upi_id": "",
  "irn": "",
  "qr_code_present": "",
  "payment_terms": "",
  "due_date": ""
}
```

## 18. Recommended Fraud Rules

```text
Rule 1: If GST is charged but supplier GSTIN is missing → High risk.
Rule 2: If invoice number is missing → High risk.
Rule 3: If same vendor and invoice number already exist → High risk.
Rule 4: If total amount does not match recalculated amount → High risk.
Rule 5: If bank account changed from vendor master → High risk.
Rule 6: If supplier GSTIN state code does not match supplier address → Medium risk.
Rule 7: If invoice date is after today → High risk.
Rule 8: If invoice date is before purchase order date → Medium/high risk.
Rule 9: If line item description is vague for a high-value invoice → Medium risk.
Rule 10: If invoice has no PO/GRN/service proof → Medium/high risk.
Rule 11: If e-invoice required but IRN/QR missing → High risk.
Rule 12: If vendor legal name, GSTIN name, and bank name differ → High risk.
```

## 19. Best Practice for MSMEs

MSMEs should not rely only on visual invoice checking. They should maintain a vendor master, purchase order records, goods receipt notes, payment history, GSTIN verification logs, and duplicate invoice checks.

A good invoice approval workflow should include:

```text
Invoice received
→ OCR/extraction
→ Mandatory field check
→ GSTIN check
→ Math validation
→ Duplicate check
→ PO/GRN/service proof matching
→ Bank detail verification
→ Risk score
→ Manual approval if medium/high risk
→ Payment only after approval
```

## 20. Simple Summary

A fake invoice may have a wrong GSTIN, missing invoice number, mismatched totals, suspicious vendor details, duplicate invoice number, changed bank account, missing purchase order, missing delivery proof, wrong GST calculation, or missing IRN/QR code where e-invoicing applies.

For MSMEs, every invoice should be checked against three things:

```text
1. Is the vendor real?
2. Is the invoice mathematically and legally complete?
3. Did the goods or services actually happen?
```

If the answer to any of these is unclear, the invoice should be flagged for manual review before payment.
