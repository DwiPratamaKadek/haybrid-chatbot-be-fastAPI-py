import numpy as np
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


class BgeBiEmbeddingModel():
    # Load BGE bi-encoder
    def __init__(self):
        self.embeddings = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-large-en-v1.5",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    
    def semantic_filter(self, query, bm25_results, top_k=5):
        # Embed query
        q_emb = np.array(self.embeddings.embed_query(query))

        # Embed dokumen (BENAR)
        texts = [d.page_content for d in bm25_results]
        doc_embs = self.embeddings.embed_documents(texts)

        # Hitung similarity
        scores = []
        for doc, emb in zip(bm25_results, doc_embs):
            score = np.dot(q_emb, emb)  # cosine similarity
            scores.append((doc, score))

        # Sorting
        scores.sort(key=lambda x: x[1], reverse=True)

        # Return Document saja (siap reranker)
        return [doc for doc, _ in scores[:top_k]]