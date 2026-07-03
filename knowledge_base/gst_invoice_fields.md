# GST Invoice Fields

## Purpose

This document explains the mandatory fields that should appear on a GST tax invoice in India. It is intended for MSME finance, invoice processing, OCR extraction, RAG search, and validation workflows.

A GST tax invoice is a legal/commercial document issued by a registered supplier for taxable supply of goods or services. Under Rule 46 of the CGST Rules, a tax invoice must contain specific supplier, recipient, invoice, item, value, tax, place-of-supply, reverse-charge, signature, and QR/IRN details where applicable.

---

## Core Idea

A GST invoice should clearly answer:

1. Who is selling?
2. Who is buying?
3. What goods or services were supplied?
4. When was the invoice issued?
5. What is the taxable value?
6. Which GST taxes apply?
7. What is the tax amount?
8. Is it intra-state or inter-state supply?
9. Is reverse charge applicable?
10. Is e-invoicing/IRN/QR code required?

---

## Mandatory Supplier Details

Every GST tax invoice should contain the supplier’s:

* Supplier name
* Supplier address
* Supplier GSTIN

The GSTIN identifies the registered supplier under GST. Rule 46 specifically requires the name, address, and GSTIN of the supplier.

### Example

```text
Supplier Name: ABC Traders Pvt Ltd
Supplier Address: 25 Industrial Area, Jaipur, Rajasthan
Supplier GSTIN: 08ABCDE1234F1Z5
```

---

## Mandatory Invoice Identification Details

A GST invoice must have a unique invoice number and issue date.

### Invoice Number

The invoice number should be:

* Consecutive
* Unique for a financial year
* Not more than 16 characters
* Allowed to contain alphabets, numbers, hyphen `-`, slash `/`, or combinations of these

Rule 46 requires a consecutive serial number, unique for a financial year, not exceeding 16 characters.

### Invoice Date

The invoice must show the date of issue.

### Example

```text
Invoice Number: INV-2025-0012
Invoice Date: 15-07-2025
```

### RAG Keywords

```text
invoice number, invoice serial number, tax invoice number, issue date, invoice date, unique invoice number, financial year invoice series
```

---

## Mandatory Recipient Details

Recipient details depend on whether the buyer is registered or unregistered.

### Registered Recipient

If the recipient is registered under GST, the invoice should contain:

* Recipient name
* Recipient address
* Recipient GSTIN or UIN, if applicable

Rule 46 requires name, address, and GSTIN or UIN of the recipient if the recipient is registered.

### Unregistered Recipient

If the recipient is unregistered and the taxable supply value is ₹50,000 or more, the invoice should contain:

* Recipient name
* Recipient address
* Delivery address
* State name
* State code

If the taxable supply is less than ₹50,000, these details are required when the recipient asks for them to be recorded.

### Example

```text
Recipient Name: XYZ Retail Store
Recipient Address: MG Road, Pune, Maharashtra
Recipient GSTIN: 27XYZAB1234C1Z8
Place of Delivery: Pune, Maharashtra
State Code: 27
```

---

## Item or Line-Item Details

Each invoice should describe what was supplied. For goods and services, the invoice should contain:

* HSN/SAC code
* Description of goods or services
* Quantity, in case of goods
* Unit or Unique Quantity Code, where applicable
* Total value
* Taxable value

Rule 46 requires HSN code for goods or services, description, quantity for goods, total value, and taxable value after discount or abatement.

### HSN and SAC

HSN stands for Harmonised System of Nomenclature. It is used for classifying goods.

SAC stands for Services Accounting Code. It is commonly used for classifying services.

In GST invoices, HSN/SAC helps identify the correct tax classification and applicable GST rate.

### Example Line Item

```text
Description: LED Monitor 24 inch
HSN Code: 85285200
Quantity: 5
Unit: PCS
Unit Price: ₹8,000
Total Value: ₹40,000
Discount: ₹2,000
Taxable Value: ₹38,000
GST Rate: 18%
```

---

## Value Fields

A GST invoice usually contains multiple value-related fields.

### Total Value

Total value means the gross value of goods or services before adjusting GST tax details.

### Taxable Value

Taxable value is the value on which GST is calculated. It is generally calculated after considering discounts or abatements, if any.

Rule 46 requires both total value and taxable value, with taxable value calculated after discount or abatement where applicable.

### Common Formula

```text
Taxable Value = Total Value - Discount/Abatement
GST Amount = Taxable Value × GST Rate
Invoice Total = Taxable Value + GST Amount
```

### Example

```text
Total Value: ₹1,00,000
Discount: ₹10,000
Taxable Value: ₹90,000
GST Rate: 18%
GST Amount: ₹16,200
Invoice Total: ₹1,06,200
```

---

## GST Tax Rate Fields

A GST invoice must show the applicable tax rate. Depending on the transaction, the invoice may contain:

* CGST rate
* SGST rate
* IGST rate
* UTGST rate
* Cess rate, if applicable

Rule 46 requires the rate of tax, including central tax, state tax, integrated tax, union territory tax, or cess.

---

## GST Tax Amount Fields

A GST invoice must also show the tax amount charged.

Depending on the transaction, it may contain:

* CGST amount
* SGST amount
* IGST amount
* UTGST amount
* Cess amount, if applicable

Rule 46 requires the amount of tax charged for central tax, state tax, integrated tax, union territory tax, or cess.

### Intra-State Supply Example

When supplier and buyer are in the same state, GST is usually split into CGST and SGST.

```text
Taxable Value: ₹50,000
GST Rate: 18%
CGST: 9% = ₹4,500
SGST: 9% = ₹4,500
Total GST: ₹9,000
Invoice Total: ₹59,000
```

### Inter-State Supply Example

When supplier and buyer are in different states, IGST usually applies.

```text
Taxable Value: ₹50,000
IGST Rate: 18%
IGST Amount: ₹9,000
Invoice Total: ₹59,000
```

---

## Place of Supply

For inter-state trade or commerce, the invoice must mention the place of supply along with the state name.

Place of supply helps decide whether CGST + SGST or IGST should apply.

### Example

```text
Supplier State: Rajasthan
Recipient State: Maharashtra
Place of Supply: Maharashtra
Tax Type: IGST
```

---

## Delivery Address

If the delivery address is different from the place of supply, the invoice should mention the delivery address separately.

### Example

```text
Recipient Billing Address: Mumbai, Maharashtra
Delivery Address: Pune, Maharashtra
Place of Supply: Maharashtra
```

---

## Reverse Charge Field

The invoice must mention whether tax is payable under reverse charge.

Reverse charge means the recipient, not the supplier, is responsible for paying GST.

### Common Invoice Text

```text
Reverse Charge: Yes
```

or

```text
Reverse Charge: No
```

### RAG Keywords

```text
reverse charge, RCM, tax payable on reverse charge, recipient liable to pay GST
```

---

## Signature or Digital Signature

A GST invoice must contain the signature or digital signature of the supplier or authorised representative.

However, Rule 46 also states that signature or digital signature is not required when an electronic invoice is issued in accordance with the Information Technology Act, 2000.

### Example

```text
Authorised Signatory
For ABC Traders Pvt Ltd
```

---

## QR Code, IRN, and E-Invoice Details

For taxpayers to whom GST e-invoicing applies, the invoice should contain a QR code with embedded Invoice Reference Number, also called IRN. Rule 46 includes QR code with embedded IRN when the invoice is issued in the manner prescribed under Rule 48(4).

The GST e-Invoice System is used by GST registered persons to upload B2B invoices to the Invoice Registration Portal. The IRP returns a unique IRN, digitally signed e-invoice, and QR code.

### Current E-Invoice Applicability Signal

The e-Invoice portal lists notified Annual Aggregate Turnover groups and dates. It shows e-invoicing from ₹5 crore to ₹10 crore as applicable from 01-08-2023, while less than ₹5 crore is optional.

### IRN Meaning

IRN means Invoice Reference Number. It is a unique identifier generated for an e-invoice.

### QR Code Meaning

The QR code helps verify key e-invoice details digitally. The e-Invoice user manual explains that the system generates a unique 64-character IRN and digitally signs the e-invoice and QR code.

### Example E-Invoice Fields

```text
IRN: 64-character invoice reference number
Ack No: Acknowledgement number from IRP
Ack Date: Date of acknowledgement
Signed QR Code: QR code generated by IRP
```

---

## Export Invoice Fields

For export of goods or services, the invoice should carry a suitable export endorsement. Rule 46 states that export invoices should carry endorsement text for supply meant for export or SEZ supply, either on payment of integrated tax or under bond/Letter of Undertaking without payment of integrated tax.

The export invoice should contain:

* Name and address of recipient
* Address of delivery
* Country of destination

Rule 46 specifically lists these details for export cases.

### Example Export Endorsement

```text
SUPPLY MEANT FOR EXPORT ON PAYMENT OF INTEGRATED TAX
```

or

```text
SUPPLY MEANT FOR EXPORT UNDER BOND OR LETTER OF UNDERTAKING WITHOUT PAYMENT OF INTEGRATED TAX
```

---

## Consolidated Tax Invoice

In some cases, a registered person may issue a consolidated tax invoice at the close of the day for certain supplies where the recipient is not registered and does not require an invoice. Rule 46 mentions this for supplies covered by the specified conditions.

### Simple Explanation

For small B2C sales where the customer does not ask for a tax invoice, the business may issue one consolidated invoice for the day, if the legal conditions are satisfied.

---

## Difference Between Tax Invoice and Bill of Supply

A tax invoice is generally issued for taxable supplies where GST is charged.

A bill of supply is generally issued when GST is not charged, such as by a composition taxpayer or for exempt supply. CBIC invoice rules list separate fields for bill of supply, including supplier name/address/GSTIN, serial number, date, recipient details, HSN/accounting code, description, value, and signature.

---

## RAG Extraction Schema

Use this schema when extracting GST invoice fields from PDFs, images, OCR text, or structured invoice data.

```json
{
  "document_type": "tax_invoice",
  "supplier": {
    "name": "",
    "address": "",
    "gstin": ""
  },
  "recipient": {
    "name": "",
    "address": "",
    "gstin_or_uin": "",
    "is_registered": null
  },
  "invoice": {
    "invoice_number": "",
    "invoice_date": "",
    "financial_year": "",
    "is_unique_number": null
  },
  "items": [
    {
      "description": "",
      "hsn_or_sac": "",
      "quantity": null,
      "unit": "",
      "total_value": null,
      "discount": null,
      "taxable_value": null,
      "gst_rate": null,
      "cgst_rate": null,
      "sgst_rate": null,
      "igst_rate": null,
      "cess_rate": null,
      "cgst_amount": null,
      "sgst_amount": null,
      "igst_amount": null,
      "cess_amount": null,
      "line_total": null
    }
  ],
  "tax_summary": {
    "total_value": null,
    "total_taxable_value": null,
    "total_cgst": null,
    "total_sgst": null,
    "total_igst": null,
    "total_cess": null,
    "total_tax": null,
    "invoice_total": null
  },
  "supply_details": {
    "place_of_supply": "",
    "state_name": "",
    "state_code": "",
    "delivery_address": "",
    "is_inter_state": null
  },
  "reverse_charge": {
    "applicable": null
  },
  "einvoice": {
    "applicable": null,
    "irn": "",
    "ack_number": "",
    "ack_date": "",
    "qr_code_present": null
  },
  "signature": {
    "present": null,
    "type": "physical_or_digital_or_not_required_for_einvoice"
  }
}
```

---

## Validation Rules for AI/OCR Systems

### Rule 1: Supplier GSTIN should be present

If the supplier is GST registered and issuing a GST tax invoice, supplier GSTIN is mandatory.

### Rule 2: Invoice number should not be missing

A missing invoice number makes tracking, accounting, GST return filing, and audit matching difficult.

### Rule 3: Invoice date should be present

Invoice date is required for tax period, due date, GST return mapping, and accounting period.

### Rule 4: Recipient GSTIN matters for B2B

For B2B invoices, recipient GSTIN is important because the invoice may be used for input tax credit matching.

### Rule 5: Taxable value and tax amount should match

Check whether:

```text
GST Amount = Taxable Value × GST Rate
```

For CGST + SGST invoices:

```text
Total GST = CGST Amount + SGST Amount
```

For IGST invoices:

```text
Total GST = IGST Amount
```

### Rule 6: Place of supply controls tax type

If supplier state and place of supply are the same, CGST + SGST usually applies.

If supplier state and place of supply are different, IGST usually applies.

### Rule 7: Reverse charge must be explicitly checked

The invoice should state whether reverse charge is applicable.

### Rule 8: E-invoice data should be checked where applicable

If e-invoicing applies, check for:

* IRN
* QR code
* Acknowledgement number/date, if available

---

## Common OCR Field Names and Aliases

| Standard Field  | Common Invoice Labels                              |
| --------------- | -------------------------------------------------- |
| Supplier Name   | Seller, Vendor, Billed By, From                    |
| Supplier GSTIN  | GSTIN, GST No, GST Number, Supplier GSTIN          |
| Recipient Name  | Buyer, Customer, Billed To, Consignee              |
| Recipient GSTIN | Buyer GSTIN, Customer GSTIN, GST No                |
| Invoice Number  | Invoice No, Bill No, Tax Invoice No, Inv No        |
| Invoice Date    | Date, Bill Date, Invoice Dt                        |
| HSN/SAC         | HSN, SAC, HSN Code, SAC Code                       |
| Description     | Item, Particulars, Product, Service                |
| Quantity        | Qty, QTY, Quantity                                 |
| Unit            | UOM, Unit, PCS, KG, NOS                            |
| Taxable Value   | Taxable Amount, Assessable Value, Taxable Amt      |
| GST Rate        | Rate, GST %, Tax Rate                              |
| CGST            | Central Tax, CGST Amount                           |
| SGST            | State Tax, SGST Amount                             |
| IGST            | Integrated Tax, IGST Amount                        |
| Cess            | Compensation Cess, Cess Amount                     |
| Place of Supply | POS, Supply State, Place of Supply                 |
| Reverse Charge  | RCM, Reverse Charge, Tax Payable on Reverse Charge |
| IRN             | Invoice Reference Number, IRN No                   |
| QR Code         | Signed QR Code, E-Invoice QR                       |

---

## Common User Questions This File Should Answer

### What fields are mandatory on a GST invoice?

A GST invoice must include supplier details, invoice number, invoice date, recipient details, HSN/SAC, description, quantity for goods, total value, taxable value, tax rate, tax amount, place of supply for inter-state supply, delivery address where different, reverse-charge status, signature/digital signature, and QR/IRN details where e-invoicing applies.

### Is GSTIN mandatory on an invoice?

Supplier GSTIN is mandatory on a GST tax invoice. Recipient GSTIN is required when the recipient is registered.

### Is HSN mandatory on a GST invoice?

Rule 46 requires HSN code for goods or services, while the number of digits may be specified by notification for different classes of taxpayers or supplies.

### Is QR code mandatory on every GST invoice?

No. QR code/IRN is required where e-invoicing provisions apply. Rule 46 refers to QR code with embedded IRN where the invoice is issued under the prescribed e-invoice manner.

### What is IRN?

IRN stands for Invoice Reference Number. It is generated by the Invoice Registration Portal for e-invoices.

### What is reverse charge?

Reverse charge means the recipient is liable to pay GST instead of the supplier. The invoice should mention whether tax is payable on reverse charge basis.

---

## Example GST Invoice Structure

```text
TAX INVOICE

Supplier:
ABC Traders Pvt Ltd
25 Industrial Area, Jaipur, Rajasthan
GSTIN: 08ABCDE1234F1Z5

Invoice No: INV-2025-0012
Invoice Date: 15-07-2025

Recipient:
XYZ Retail Store
MG Road, Pune, Maharashtra
GSTIN: 27XYZAB1234C1Z8

Place of Supply: Maharashtra
Delivery Address: Pune, Maharashtra
Reverse Charge: No

Item Details:
1. LED Monitor 24 inch
   HSN: 85285200
   Quantity: 5 PCS
   Total Value: ₹40,000
   Discount: ₹2,000
   Taxable Value: ₹38,000
   GST Rate: 18%
   IGST Amount: ₹6,840

Total Taxable Value: ₹38,000
Total IGST: ₹6,840
Invoice Total: ₹44,840

Authorised Signatory
```

---

## RAG Chunking Notes

Recommended chunk size: 500–900 tokens.

Recommended chunk overlap: 80–120 tokens.

Best chunk headings:

```text
GST Invoice Supplier Details
GST Invoice Recipient Details
GST Invoice Number and Date
GST Invoice Item Fields
GST Invoice Taxable Value
GST Invoice CGST SGST IGST
GST Invoice Place of Supply
GST Invoice Reverse Charge
GST E-Invoice IRN QR Code
GST Invoice OCR Extraction Schema
GST Invoice Validation Rules
```

---

## Source Notes

Primary legal reference: Rule 46 of the CGST Rules, which lists mandatory tax invoice particulars including supplier details, invoice serial number, issue date, recipient details, HSN, description, quantity, values, tax rate, tax amount, place of supply, delivery address, reverse charge, signature, and QR/IRN where applicable.

E-invoice reference: GST e-Invoice portal explains that B2B invoices are uploaded to the Invoice Registration Portal, which returns IRN, digitally signed e-invoice, and QR code.

E-invoice applicability reference: The e-Invoice portal’s taxpayer enablement page lists notified Annual Aggregate Turnover groups and dates, including ₹5 crore to ₹10 crore from 01-08-2023 and less than ₹5 crore as optional.
