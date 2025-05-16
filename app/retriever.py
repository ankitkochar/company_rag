from app.faiss_indexer import FAISSIndexer
from app.embedder import embed_text
from app.compressor import compress_chunks

indexer = FAISSIndexer()

def retrieve_similar_companies(query: str, top_k=10):
    embedding = embed_text(query, task_type="RETRIEVAL_QUERY")
    candidates = indexer.query(embedding, top_k=top_k)
    matched_metadata = [indexer.metadata[idx] for idx, _ in candidates]
    
    compressed = compress_chunks(query, matched_metadata)
    return compressed
