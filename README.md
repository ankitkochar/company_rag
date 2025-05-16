# 🧠 RAG-Based Company Intelligence API

A semantic search system that uses **FAISS** for fast vector retrieval and **Google Gemini** for intelligent filtering. It answers natural-language queries over a database of companies.

---

## 🚀 Features

✅ Retrieval-Augmented Generation (RAG)  
✅ Google Gemini Embeddings + Generative Reasoning  
✅ FAISS Vector DB for efficient top-k retrieval  
✅ Intelligent **chunk compression** using LLM  
✅ FastAPI-powered HTTP interface  
✅ MongoDB for structured company storage  

---

## 📦 Project Structure

```
rag_company_qa/
├── app/
│   ├── main.py             # FastAPI entrypoint
│   ├── embedder.py         # Embedding & ingestion logic
│   ├── retriever.py        # RAG retriever (FAISS + LLM filter)
│   ├── faiss_indexer.py    # Vector database management (FAISS)
│   ├── compressor.py       # LLM chunk compression filter
│   ├── config.py           # API keys and database configs
├── data/
│   └── mock_companies_data.json
├── ingest.py               # Load + flatten company data into MongoDB
├── requirements.txt
├── README.md               # ← You are here
```

---

## 🧪 Setup Instructions

### 1. Clone the repo and create a virtualenv

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up your `.env` file

```
GOOGLE_API_KEY=your-gemini-api-key
MONGO_URI=your-mongodb-uri
DB_NAME=ragdb
COLLECTION_NAME=companies
```

### 4. Ingest mock company data into MongoDB

```bash
python app\ingest.py
```

### 5. Generate and index embeddings into FAISS

```bash
python -c "from app.embedder import generate_embeddings; generate_embeddings()"
```

### 6. Start the API server

```bash
uvicorn app.main:app --reload
```

---

## ✅ API Usage

### 🔍 Endpoint

```
POST /ask
```

### 🔸 Request Body (JSON)

```json
{
  "query": "Show me companies created before 2010 having officer count grater than 3."
}
```

### 🔹 Response Body (JSON)

```json
{
  "matches": [
    {
      "company_number": "10000015",
      "company_name": "Walker, Francis and Butler",
      "company_status": "active",
      "confirmation_overdue": "False",
      "date_of_creation": "2007-11-26",
      "has_charges": "True",
      "has_insolvency_history": "True",
      "jurisdiction": "scotland",
      "last_accounts_date": "2023-10-29",
      "officer_count": "5",
      "sic_codes": "51001",
      "type": "ltd"
    },
    {
      "company_number": "10000007",
      "company_name": "Parker Ltd",
      "company_status": "liquidation",
      "confirmation_overdue": "False",
      "date_of_creation": "2009-07-17",
      "has_charges": "True",
      "has_insolvency_history": "True",
      "jurisdiction": "england-wales",
      "last_accounts_date": "2023-07-17",
      "officer_count": "5",
      "sic_codes": "85482",
      "type": "llp"
    },
    {
      "company_number": "10000008",
      "company_name": "Burns LLC",
      "company_status": "active",
      "confirmation_overdue": "True",
      "date_of_creation": "2002-12-14",
      "has_charges": "True",
      "has_insolvency_history": "False",
      "jurisdiction": "england-wales",
      "last_accounts_date": "2023-11-27",
      "officer_count": "4",
      "sic_codes": "49187",
      "type": "llp"
    }
  ]
}
```

---

## 🧠 How It Works

1. Query is embedded using **Gemini embeddings**
2. FAISS retrieves the top 10 semantically relevant candidates
3. Each candidate is passed through **Gemini LLM** with a Yes/No check:
   - "Does this record satisfy the query?"
4. Only relevant records are returned

---

## ✅ Tips

- Queries like `"active companies in England with SIC code 62020"` also work.
- Ensure your `.env` and `MongoDB` are correctly configured before running.
- Modify `compressor.py` for more verbose LLM output or explanations.

---
