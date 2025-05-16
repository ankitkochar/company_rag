import faiss
import numpy as np
import pickle
import os

class FAISSIndexer:
    def __init__(self, dim=768, index_path="faiss.index", meta_path="metadata.pkl"):
        self.dim = dim
        self.index_path = index_path
        self.meta_path = meta_path
        self.index = faiss.IndexFlatL2(dim)
        self.metadata = []

        if os.path.exists(index_path) and os.path.exists(meta_path):
            self.index = faiss.read_index(index_path)
            with open(meta_path, "rb") as f:
                self.metadata = pickle.load(f)

    def add(self, embeddings, metadatas):
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)
        self.metadata.extend(metadatas)
        self.save()

    def query(self, embedding, top_k=10):
        query_vec = np.array([embedding]).astype("float32")
        distances, indices = self.index.search(query_vec, top_k)
        return [(i, distances[0][j]) for j, i in enumerate(indices[0]) if i < len(self.metadata)]


    def save(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)
