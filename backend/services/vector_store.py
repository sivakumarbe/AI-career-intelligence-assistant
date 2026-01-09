import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []
        self.metadatas = []

    def reset(self):
        """
        Clears all vectors and metadata.
        Called before rebuilding the vector store.
        """
        self.index = faiss.IndexFlatL2(self.dim)
        self.texts = []
        self.metadatas = []

    def add(self, embeddings, texts, metadatas):
        embeddings = np.array(embeddings).astype("float32")

        
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        
        assert embeddings.ndim == 2, "Embeddings must be 2D"
        assert embeddings.shape[0] == len(texts) == len(metadatas), \
            f"Mismatch: embeddings={embeddings.shape[0]}, texts={len(texts)}, metadata={len(metadatas)}"

        self.index.add(embeddings)
        self.texts.extend(texts)
        self.metadatas.extend(metadatas)

    def search(self, query_embedding, top_k=5):
        if self.index.ntotal == 0:
            return []

        query_embedding = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_embedding, top_k)

        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            if idx >= len(self.texts):
                continue

            results.append({
                "text": self.texts[idx],
                "metadata": self.metadatas[idx]
            })

        return results



VECTOR_DIM = 384
vector_store = VectorStore(dim=VECTOR_DIM)
