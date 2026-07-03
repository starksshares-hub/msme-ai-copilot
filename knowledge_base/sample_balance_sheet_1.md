# Sample Balance Sheet 1: Healthy MSME Balance Sheet Example

This is a sample balance sheet used for training a RAG-based MSME finance assistant. It represents a small business with a reasonably healthy financial position.

A balance sheet shows what a business owns, what it owes, and what belongs to the owner at a specific date.

The basic balance sheet formula is:

```text
Assets = Liabilities + Equity
```

This sample can help an AI assistant answer questions about assets, liabilities, equity, working capital, liquidity, loans, inventory, receivables, payables, and overall financial health.

---

## Business Profile

**Business Name:** Zenith Retail Solutions
**Business Type:** MSME trading business
**Industry:** Office supplies and retail distribution
**Location:** Mumbai, Maharashtra
**Balance Sheet Date:** 31 March 2025
**Financial Year:** FY 2024-25

---

## Balance Sheet Summary

This business has:

```text
Total Assets: ₹18,50,000
Total Liabilities: ₹7,20,000
Owner's Equity: ₹11,30,000
```

Balance sheet equation check:

```text
Assets = Liabilities + Equity

₹18,50,000 = ₹7,20,000 + ₹11,30,000

₹18,50,000 = ₹18,50,000
```

The balance sheet balances correctly.

---

# Balance Sheet

## Assets

Assets are resources owned or controlled by the business. Assets may include cash, bank balance, inventory, money receivable from customers, equipment, furniture, and deposits.

---

## Current Assets

Current assets are assets expected to be converted into cash, sold, or used within one year.

| Asset Type                          |         Amount |
| ----------------------------------- | -------------: |
| Cash in Hand                        |        ₹75,000 |
| Bank Balance                        |      ₹3,25,000 |
| Accounts Receivable / Trade Debtors |      ₹4,20,000 |
| Inventory / Stock                   |      ₹5,10,000 |
| Prepaid Expenses                    |        ₹40,000 |
| GST Input Tax Credit Receivable     |        ₹80,000 |
| **Total Current Assets**            | **₹14,50,000** |

---

## Non-Current Assets

Non-current assets are long-term assets used in the business for more than one year.

| Asset Type                       |        Amount |
| -------------------------------- | ------------: |
| Furniture and Fixtures           |     ₹1,20,000 |
| Computers and Billing Equipment  |     ₹1,50,000 |
| Office Equipment                 |       ₹60,000 |
| Security Deposit for Shop/Office |       ₹70,000 |
| **Total Non-Current Assets**     | **₹4,00,000** |

---

## Total Assets

```text
Total Assets = Total Current Assets + Total Non-Current Assets

Total Assets = ₹14,50,000 + ₹4,00,000

Total Assets = ₹18,50,000
```

| Category                 |         Amount |
| ------------------------ | -------------: |
| Total Current Assets     |     ₹14,50,000 |
| Total Non-Current Assets |      ₹4,00,000 |
| **Total Assets**         | **₹18,50,000** |

---

# Liabilities

Liabilities are amounts the business owes to outsiders. These may include supplier dues, loans, GST payable, salary payable, rent payable, and other obligations.

---

## Current Liabilities

Current liabilities are obligations expected to be paid within one year.

| Liability Type                     |        Amount |
| ---------------------------------- | ------------: |
| Accounts Payable / Trade Creditors |     ₹2,70,000 |
| Short-Term Business Loan           |     ₹1,50,000 |
| GST Payable                        |       ₹60,000 |
| Salary Payable                     |       ₹40,000 |
| Rent Payable                       |       ₹30,000 |
| Outstanding Expenses               |       ₹20,000 |
| **Total Current Liabilities**      | **₹5,70,000** |

---

## Non-Current Liabilities

Non-current liabilities are long-term obligations payable after one year.

| Liability Type                    |        Amount |
| --------------------------------- | ------------: |
| Long-Term Business Loan           |     ₹1,50,000 |
| **Total Non-Current Liabilities** | **₹1,50,000** |

---

## Total Liabilities

```text
Total Liabilities = Current Liabilities + Non-Current Liabilities

Total Liabilities = ₹5,70,000 + ₹1,50,000

Total Liabilities = ₹7,20,000
```

| Category                      |        Amount |
| ----------------------------- | ------------: |
| Total Current Liabilities     |     ₹5,70,000 |
| Total Non-Current Liabilities |     ₹1,50,000 |
| **Total Liabilities**         | **₹7,20,000** |

---

# Owner's Equity

Equity is the owner’s claim in the business after paying all liabilities. It includes capital introduced by the owner and retained profits.

| Equity Type                            |         Amount |
| -------------------------------------- | -------------: |
| Owner's Capital                        |      ₹8,00,000 |
| Retained Earnings / Accumulated Profit |      ₹3,30,000 |
| **Total Owner's Equity**               | **₹11,30,000** |

---

## Total Liabilities and Equity

```text
Total Liabilities and Equity = Total Liabilities + Owner's Equity

Total Liabilities and Equity = ₹7,20,000 + ₹11,30,000

Total Liabilities and Equity = ₹18,50,000
```

| Category                         |         Amount |
| -------------------------------- | -------------: |
| Total Liabilities                |      ₹7,20,000 |
| Owner's Equity                   |     ₹11,30,000 |
| **Total Liabilities and Equity** | **₹18,50,000** |

---

# Balance Sheet Equation Validation

```text
Assets = Liabilities + Equity

Assets = ₹18,50,000
Liabilities = ₹7,20,000
Equity = ₹11,30,000

Liabilities + Equity = ₹7,20,000 + ₹11,30,000
Liabilities + Equity = ₹18,50,000

Therefore:

₹18,50,000 = ₹18,50,000
```

The balance sheet is valid because total assets equal total liabilities plus owner’s equity.

---

# Extracted JSON Example

```json
{
  "business_name": "Zenith Retail Solutions",
  "business_type": "MSME trading business",
  "industry": "Office supplies and retail distribution",
  "balance_sheet_date": "2025-03-31",
  "financial_year": "FY 2024-25",
  "assets": {
    "current_assets": {
      "cash_in_hand": 75000,
      "bank_balance": 325000,
      "accounts_receivable": 420000,
      "inventory": 510000,
      "prepaid_expenses": 40000,
      "gst_input_tax_credit_receivable": 80000,
      "total_current_assets": 1450000
    },
    "non_current_assets": {
      "furniture_and_fixtures": 120000,
      "computers_and_billing_equipment": 150000,
      "office_equipment": 60000,
      "security_deposit": 70000,
      "total_non_current_assets": 400000
    },
    "total_assets": 1850000
  },
  "liabilities": {
    "current_liabilities": {
      "accounts_payable": 270000,
      "short_term_business_loan": 150000,
      "gst_payable": 60000,
      "salary_payable": 40000,
      "rent_payable": 30000,
      "outstanding_expenses": 20000,
      "total_current_liabilities": 570000
    },
    "non_current_liabilities": {
      "long_term_business_loan": 150000,
      "total_non_current_liabilities": 150000
    },
    "total_liabilities": 720000
  },
  "equity": {
    "owners_capital": 800000,
    "retained_earnings": 330000,
    "total_equity": 1130000
  },
  "total_liabilities_and_equity": 1850000,
  "balance_sheet_valid": true
}
```

---

# Financial Ratio Analysis

## 1. Working Capital

Working capital shows whether the business has enough short-term assets to pay short-term liabilities.

```text
Working Capital = Current Assets - Current Liabilities

Working Capital = ₹14,50,000 - ₹5,70,000

Working Capital = ₹8,80,000
```

**Result:** Positive working capital.

This means the business has more short-term assets than short-term obligations.

---

## 2. Current Ratio

Current ratio measures short-term liquidity.

```text
Current Ratio = Current Assets / Current Liabilities

Current Ratio = ₹14,50,000 / ₹5,70,000

Current Ratio = 2.54
```

**Result:** Healthy.

A current ratio of 2.54 means the business has ₹2.54 of current assets for every ₹1 of current liabilities.

---

## 3. Quick Ratio

Quick ratio checks liquidity without counting inventory.

```text
Quick Assets = Current Assets - Inventory

Quick Assets = ₹14,50,000 - ₹5,10,000

Quick Assets = ₹9,40,000

Quick Ratio = Quick Assets / Current Liabilities

Quick Ratio = ₹9,40,000 / ₹5,70,000

Quick Ratio = 1.65
```

**Result:** Good.

The business has enough liquid assets even without relying on selling inventory.

---

## 4. Debt-to-Equity Ratio

Debt-to-equity ratio shows how much the business depends on borrowed funds compared to owner funds.

```text
Debt-to-Equity Ratio = Total Liabilities / Owner's Equity

Debt-to-Equity Ratio = ₹7,20,000 / ₹11,30,000

Debt-to-Equity Ratio = 0.64
```

**Result:** Moderate and acceptable.

The business is not overly dependent on debt.

---

## 5. Inventory Share of Current Assets

This shows how much of current assets are locked in stock.

```text
Inventory Share = Inventory / Current Assets × 100

Inventory Share = ₹5,10,000 / ₹14,50,000 × 100

Inventory Share = 35.17%
```

**Result:** Normal for a trading business.

Inventory is important for a retail/distribution business, but too much inventory can create cash flow pressure.

---

## 6. Receivables Share of Current Assets

This shows how much money is pending from customers.

```text
Receivables Share = Accounts Receivable / Current Assets × 100

Receivables Share = ₹4,20,000 / ₹14,50,000 × 100

Receivables Share = 28.97%
```

**Result:** Manageable.

The business should still monitor customer payments to avoid cash flow problems.

---

# Interpretation for MSME Finance Assistant

This balance sheet shows a financially stable MSME.

The business has enough current assets to pay short-term liabilities. Its working capital is positive, current ratio is healthy, and debt level is not too high.

The main areas to monitor are accounts receivable and inventory. If customers delay payments or stock moves slowly, cash flow may become tight even if the balance sheet looks healthy.

---

# Strengths in This Balance Sheet

## 1. Positive Working Capital

The business has ₹8,80,000 positive working capital.

This means it can likely pay suppliers, rent, salaries, GST dues, and other short-term obligations.

## 2. Good Bank Balance

The business has ₹3,25,000 in bank balance and ₹75,000 cash in hand.

This gives the business immediate liquidity.

## 3. Manageable Debt

Total liabilities are ₹7,20,000 while owner’s equity is ₹11,30,000.

This means the owner has more money invested in the business than the amount owed to outsiders.

## 4. Reasonable Inventory

Inventory of ₹5,10,000 is normal for a trading business.

The business has enough stock to sell, but it should track slow-moving and dead stock.

## 5. Accounts Receivable Are Not Too High

Accounts receivable of ₹4,20,000 is significant but not extreme compared to total current assets.

The business should still follow up with customers and avoid long payment delays.

---

# Weaknesses or Risks

## 1. Receivables May Cause Cash Flow Pressure

Even though accounts receivable are assets, they are not cash yet.

If customers delay payment, the business may struggle to pay suppliers or expenses.

## 2. Inventory Can Become Dead Stock

Inventory is useful only if it sells.

If ₹5,10,000 stock includes slow-moving products, cash may get blocked.

## 3. GST Payable Must Be Paid on Time

GST payable of ₹60,000 is a short-term liability.

The business must ensure it has enough cash before GST return/payment deadlines.

## 4. Supplier Payables Need Monitoring

Accounts payable of ₹2,70,000 means the business owes money to suppliers.

Late supplier payment can damage credit terms and vendor relationships.

---

# AI Assistant Answers Based on This Balance Sheet

## Question: Is this business financially healthy?

Answer: Yes, this business appears financially healthy. It has total assets of ₹18,50,000, total liabilities of ₹7,20,000, and owner’s equity of ₹11,30,000. It also has positive working capital of ₹8,80,000 and a healthy current ratio of 2.54.

---

## Question: What is the working capital of this business?

Answer: Working capital is ₹8,80,000.

```text
Working Capital = Current Assets - Current Liabilities
Working Capital = ₹14,50,000 - ₹5,70,000
Working Capital = ₹8,80,000
```

---

## Question: Can this business pay its short-term liabilities?

Answer: Yes, it likely can. The business has current assets of ₹14,50,000 and current liabilities of ₹5,70,000. Its current ratio is 2.54, which means it has ₹2.54 of current assets for every ₹1 of current liabilities.

---

## Question: What are the biggest assets of this business?

Answer: The biggest assets are inventory of ₹5,10,000, accounts receivable of ₹4,20,000, and bank balance of ₹3,25,000.

---

## Question: What are the biggest liabilities?

Answer: The biggest liabilities are accounts payable of ₹2,70,000, short-term business loan of ₹1,50,000, and long-term business loan of ₹1,50,000.

---

## Question: Is the business too dependent on loans?

Answer: No, the business does not appear too dependent on loans. Total liabilities are ₹7,20,000 while owner’s equity is ₹11,30,000. The debt-to-equity ratio is 0.64, which is moderate.

---

## Question: What should the owner watch carefully?

Answer: The owner should watch customer receivables, inventory movement, supplier payables, GST payable, and short-term loan repayment. These items directly affect cash flow.

---

## Question: Does the balance sheet balance?

Answer: Yes. Total assets are ₹18,50,000 and total liabilities plus equity are also ₹18,50,000.

---

# RAG Training Notes

This file can help the RAG assistant answer questions about:

```text
- Balance sheet basics
- Assets
- Current assets
- Non-current assets
- Liabilities
- Current liabilities
- Non-current liabilities
- Owner's equity
- Working capital
- Current ratio
- Quick ratio
- Debt-to-equity ratio
- Inventory analysis
- Receivables analysis
- MSME financial health
- Short-term liquidity
- Balance sheet equation
```

---

# Risk Score

```text
Financial Health Risk: Low
Liquidity Risk: Low
Debt Risk: Medium-low
Inventory Risk: Medium
Receivables Risk: Medium
Overall Risk Level: Low to Medium
```

---

# Simple Summary

This sample balance sheet shows a healthy MSME.

The business owns ₹18,50,000 in assets, owes ₹7,20,000 in liabilities, and has owner’s equity of ₹11,30,000.

The balance sheet is correct because:

```text
Assets = Liabilities + Equity
₹18,50,000 = ₹7,20,000 + ₹11,30,000
```

The business has positive working capital, good liquidity, manageable debt, and enough assets to cover its liabilities.

However, the owner should still monitor receivables and inventory because delayed customer payments or slow-moving stock can create cash flow problems.
