# RAG Design for MSME AI Finance Copilot

## 1. Purpose

This document explains the RAG architecture for the MSME AI Finance Copilot.

RAG means Retrieval-Augmented Generation. Instead of asking the AI model to answer only from its memory, we first retrieve useful business documents, invoice data, GST files, payment records, or knowledge base content. Then we give that retrieved context to the AI model so it can generate a more accurate and business-specific answer.

The goal is to help small Indian businesses ask questions like:

* Why is my cash flow low this month?
* Which invoices are unpaid?
* Which vendor payments are pending?
* What GST documents are missing?
* Which products are affecting profit?
* What should I do to improve working capital?

---

## 2. RAG Architecture Diagram

```text
                 ┌──────────────────────────┐
                 │        User Query         │
                 │ Example: "Why is my       │
                 │ cash flow low this month?"│
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Query Processing Layer    │
                 │ - Clean query             │
                 │ - Detect intent           │
                 │ - Add filters if needed   │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Embedding Model           │
                 │ Converts query into       │
                 │ numerical vector          │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Vector Database           │
                 │ ChromaDB                  │
                 │ - Stores document chunks  │
                 │ - Stores embeddings       │
                 │ - Stores metadata         │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Retriever                 │
                 │ Finds top relevant chunks │
                 │ using similarity search   │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Prompt Builder            │
                 │ Combines:                 │
                 │ - User question           │
                 │ - Retrieved context       │
                 │ - System instructions     │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ LLM / AI Model            │
                 │ Generates final answer    │
                 │ using retrieved context   │
                 └────────────┬─────────────┘
                              │
                              ▼
                 ┌──────────────────────────┐
                 │ Final Business Answer     │
                 │ Clear, grounded, useful   │
                 │ response for MSME owner   │
                 └──────────────────────────┘
```

---

## 3. Retrieval Flow

The retrieval flow explains how the system answers a user question.

### Step 1: User asks a question

Example:

```text
Why is my cash flow low this month?
```

### Step 2: System converts the question into an embedding

The user query is converted into a numerical vector using an embedding model.

This helps the system compare the meaning of the question with the meaning of stored document chunks.

### Step 3: ChromaDB searches relevant chunks

ChromaDB searches the stored embeddings and finds the most relevant chunks.

Example retrieved chunks may include:

* unpaid invoice records
* high vendor payments
* low sales this month
* delayed customer payments
* inventory purchase records
* GST payment entries

### Step 4: Retrieved context is passed to the LLM

The system gives the AI model both the user question and the retrieved business context.

Example:

```text
User question:
Why is my cash flow low this month?

Retrieved context:
- Invoice INV-102 worth ₹45,000 is unpaid.
- Vendor payment of ₹30,000 was made this week.
- Sales decreased by 18% compared to last month.
- Inventory purchase increased by ₹22,000.
```

### Step 5: AI generates grounded answer

The AI gives a useful answer based on the retrieved data.

Example:

```text
Your cash flow is low mainly because customer invoice INV-102 worth ₹45,000 is still unpaid, while vendor payments and inventory purchases increased this month. Sales also dropped by 18%, which reduced incoming cash.
```

---

## 4. Chunking Strategy

Chunking means splitting large documents into smaller parts before storing them in the vector database.

This is important because the AI should retrieve only the most useful part of the document, not the full document every time.

### Documents to chunk

The system may chunk:

* invoices
* GST documents
* sales reports
* purchase reports
* vendor payment records
* customer payment records
* inventory files
* business policy documents
* financial notes

### Recommended chunk size

For this project, the starting chunking strategy will be:

```text
Chunk size: 500 to 800 tokens
Chunk overlap: 100 to 150 tokens
```

### Why use overlap?

Overlap helps avoid losing important meaning between two chunks.

Example:

If one chunk ends with invoice details and the next chunk starts with payment status, overlap helps keep both connected.

### Metadata stored with each chunk

Each chunk should store metadata such as:

```text
source_file
document_type
business_name
date
month
year
invoice_id
customer_name
vendor_name
gst_period
page_number
created_at
```

### Example chunk

```json
{
  "page_content": "Invoice INV-102 for customer ABC Traders worth ₹45,000 is unpaid since 15 June 2026.",
  "metadata": {
    "source_file": "june_invoices.pdf",
    "document_type": "invoice",
    "invoice_id": "INV-102",
    "customer_name": "ABC Traders",
    "month": "June",
    "year": "2026"
  }
}
```

---

## 5. Embedding Model Selection

The embedding model converts text into numerical vectors so similar meanings can be searched.

For the first version of the project, the recommended model is:

```text
text-embedding-3-small
```

### Why this model?

* Good balance between quality and cost
* Suitable for semantic search
* Works well for retrieval-based applications
* Fast enough for an MVP
* Useful for documents like invoices, reports, notes, and financial text

### Future embedding options

Later, the system can test other embedding models:

```text
text-embedding-3-large
```

Useful when higher retrieval accuracy is needed.

```text
bge-small / bge-base / bge-large
```

Useful if we want open-source local embeddings.

```text
nomic-embed-text
```

Useful if we want local or open-source embedding experiments.

### Final decision for MVP

For the MVP, use:

```text
text-embedding-3-small
```

Reason:

It is simple, fast, cost-effective, and good enough for a first working RAG prototype.

---

## 6. Why ChromaDB?

ChromaDB is selected as the vector database for the MVP.

### Reasons for choosing ChromaDB

* Easy to install and use with Python
* Good for learning and prototyping RAG systems
* Works well with LangChain
* Can store documents, embeddings, and metadata
* Supports similarity search
* Supports metadata filtering
* Can run locally during development
* Does not require complex cloud setup for the first version

### Why it fits this MSME project

For an MSME AI Finance Copilot, we need to search business documents quickly.

ChromaDB can help retrieve relevant records like:

* unpaid invoices
* customer payment history
* GST-related documents
* vendor bills
* sales records
* purchase records
* inventory notes

Example:

```text
User asks:
Which invoices are still unpaid?

ChromaDB retrieves:
Chunks where document_type = invoice and payment_status = unpaid.
```

This makes the AI answer more accurate because it uses actual business data instead of guessing.

---

## 7. Future Improvements

The first RAG version should be simple. Later, the system can be improved.

### 1. Hybrid search

Use both semantic search and keyword search.

This helps when exact words matter.

Example:

```text
INV-102
GST
ABC Traders
June 2026
```

### 2. Metadata filtering

Use filters like:

```text
month = June
document_type = invoice
customer_name = ABC Traders
payment_status = unpaid
```

This will improve accuracy.

### 3. Reranking

After retrieving chunks, use a reranker to sort the best results more accurately.

This reduces irrelevant context.

### 4. Better document loaders

Support more file types:

* PDF
* Excel
* CSV
* images
* scanned invoices
* GST reports

### 5. OCR support

Add OCR for scanned invoices and paper bills.

This will help small businesses that still use physical documents.

### 6. Automatic data refresh

When new invoices, payments, or GST files are added, the vector database should update automatically.

### 7. Source citations

The AI should show which document or invoice it used.

Example:

```text
Source: june_invoices.pdf, Invoice INV-102
```

### 8. User-specific business memory

Each MSME should have separate data.

One business should not access another business's financial records.

### 9. Evaluation system

Create test questions to check if the RAG system gives correct answers.

Example:

```text
Question: Which invoice is unpaid?
Expected answer: INV-102
```

---

## 8. Risks

RAG improves accuracy, but it does not remove all problems.

### 1. Hallucinations

The AI may still generate wrong information if the retrieved context is weak or confusing.

#### Solution

* Tell the model to answer only from provided context
* Add source citations
* Return "I do not have enough data" when context is missing
* Use better retrieval and reranking

---

### 2. Stale data

The system may answer using old invoices or outdated business records.

Example:

An invoice may already be paid, but the vector database still shows it as unpaid.

#### Solution

* Update embeddings whenever documents change
* Store document timestamps
* Add latest payment status from database
* Use freshness filters

---

### 3. Missing context

The system may not retrieve the right chunk.

Example:

The user asks about cash flow, but only sales records are retrieved and payment records are missed.

#### Solution

* Improve chunking
* Add metadata filters
* Retrieve more chunks
* Use hybrid search
* Use reranking
* Improve document structure

---

### 4. Poor chunking

Bad chunking can split important information.

Example:

Invoice amount is in one chunk and payment status is in another chunk.

#### Solution

* Use chunk overlap
* Keep related invoice fields together
* Use structured extraction for invoices and financial records

---

### 5. Privacy risk

MSME financial data is sensitive.

#### Solution

* Keep local development data private
* Do not expose documents publicly
* Use environment variables for API keys
* Add user-level access control
* Separate data by business account

---

### 6. Wrong metadata

If metadata is incorrect, retrieval can fail.

Example:

A paid invoice is marked as unpaid.

#### Solution

* Validate extracted metadata
* Allow manual correction
* Keep original source documents
* Add checks before final answer

---

## 9. MVP RAG Pipeline

For the first version, the pipeline will be:

```text
1. Load MSME documents
2. Split documents into chunks
3. Create embeddings
4. Store embeddings in ChromaDB
5. Accept user question through FastAPI
6. Convert question into embedding
7. Retrieve top relevant chunks
8. Send context + question to LLM
9. Return final answer with sources
```

---

## 10. Example Use Case

### User question

```text
Why is my cash flow low this month?
```

### Retrieved context

```text
- Sales decreased by 18% in June.
- Invoice INV-102 worth ₹45,000 is unpaid.
- Vendor payment of ₹30,000 was completed.
- Inventory purchase increased by ₹22,000.
```

### AI answer

```text
Your cash flow is low because incoming cash reduced and outgoing payments increased. Sales dropped by 18%, invoice INV-102 worth ₹45,000 is still unpaid, and vendor plus inventory payments increased this month.
```

---

## 11. Final Design Decision

The first version of the MSME AI Finance Copilot will use:

```text
Backend: FastAPI
RAG Framework: LangChain
Vector Database: ChromaDB
Embedding Model: text-embedding-3-small
Document Storage: Local files for MVP
Use Case: MSME finance document question answering
```

This design is simple enough for an MVP but strong enough to later grow into a real AI finance copilot for small Indian businesses.
