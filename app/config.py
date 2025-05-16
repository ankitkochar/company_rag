import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = "ragdb"
COLLECTION_NAME = "companies"
CHROMA_COLLECTION = "company_embeddings"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
