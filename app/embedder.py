import os
import google.generativeai as genai
from dotenv import load_dotenv
from pymongo import MongoClient
from app.config import GOOGLE_API_KEY, MONGO_URI, DB_NAME, COLLECTION_NAME
from app.faiss_indexer import FAISSIndexer

load_dotenv()
genai.configure(api_key=GOOGLE_API_KEY)

indexer = FAISSIndexer()

def build_document(company):
    return (
        f"{company['company_name']} is a {company['type']} company in {company['jurisdiction']}, "
        f"created on {company['date_of_creation']}. Status: {company['company_status']}, "
        f"SIC code: {company['sic_codes']}. Confirmation overdue: {company['confirmation_overdue']}. "
        f"Last accounts filed on: {company['last_accounts_date']}. Number of officers: {company['officer_count']}."
    )

def embed_text(text: str, task_type: str):
    kwargs = {
        "model": "models/embedding-001",
        "content": text,
        "task_type": task_type
    }

    # Only include title for RETRIEVAL_DOCUMENT
    if task_type == "RETRIEVAL_DOCUMENT":
        kwargs["title"] = "Company Info"

    response = genai.embed_content(**kwargs)
    return response["embedding"]

def generate_embeddings():
    client = MongoClient(MONGO_URI)
    companies = list(client[DB_NAME][COLLECTION_NAME].find({}))
    print(f"Found {len(companies)} companies in MongoDB.")

    for idx, c in enumerate(companies):
        try:
            doc_text = build_document(c)
            embedding = embed_text(doc_text, task_type="RETRIEVAL_DOCUMENT")

            metadata_clean = {k: str(v) for k, v in c.items() if k != "_id"}
            indexer.add([embedding], [metadata_clean])
            print(f"[{idx+1}] ✅ Embedded and added: {c['company_name']}")
        except Exception as e:
            print(f"[{idx+1}] ❌ Error: {e}")

    print(f"\n✅ All embeddings inserted into FAISS.")
