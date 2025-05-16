from fastapi import FastAPI
from pydantic import BaseModel
from app.retriever import retrieve_similar_companies

app = FastAPI()

class AskRequest(BaseModel):
    query: str

@app.post("/ask")
def ask_company_info(request: AskRequest):
    results = retrieve_similar_companies(request.query, top_k=10)
    return {"matches": results}
