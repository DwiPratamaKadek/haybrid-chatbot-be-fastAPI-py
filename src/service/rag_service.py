from src.model.ml.Bm25Model import Bm25Model
from src.model.ml.BgeBiEmbeddingModel import BgeBiEmbeddingModel
from src.model.ml.CrossReranking import CrossReranker
from src.model.crud.HistoryCrud import create

from src.service.GeminiService import GeminiService

import pandas as pd 
import os

class RAGhybrid : 
    def __init__(self):
        self.data = self._load_documents()

        self.bm25 = Bm25Model(self.data)
        self.biEncoder = BgeBiEmbeddingModel()
        self.crossRerank = CrossReranker()
        self.gemini = GeminiService()

    def _load_documents(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.join(BASE_DIR, "../../dataset")

        all_docs = []

        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                df = pd.read_csv(os.path.join(folder_path, filename))

                text_columns = [c for c in df.columns if df[c].dtype == "object"]

                if not text_columns:
                    continue

                text_col = text_columns[0]

                all_docs.extend(df[text_col].dropna().tolist())

        return all_docs
    
    def hybrid_search(self,query : str):
        bm25_docs = self.bm25.search(query)
        semantic_docs = self.biEncoder.search(query)

        combined = bm25_docs + semantic_docs
        reranked = self.crossRerank.rerank(query, combined)

        return reranked

    def chat(self, query, session=None) : 
        # 1 BM25 
        bm25_doc = self.bm25.retrieve(query)
        # 2 Bi embeding 
        bi_docs = self.biEncoder.semantic_filter(
            query,
            bm25_doc, 
            top_k=5
        )
        # cross reranking 
        reranked_docs = self.crossRerank.rerank(
            query=query,
            document=bi_docs, 
            top_k=3
        )
        if not reranked_docs: 
            return{
                "query" : query,
                "answer" : "Informasi tidak ditemukan"
            }
        # self.hybrid_search(query)        
        # Gabungkan context
        context = "\n\n".join([doc.page_content for doc in reranked_docs])
        # context = "\n\n".join([doc.page_content for doc in self.hybrid_search])
        reranked_answare = context 
      
        

        #prompt gemini 
        prompt = f"""
        Konteks:
        {context}

        Pertanyaan: {query}
        Jawaban:
        """

        answer = self.gemini.generate(prompt)

        # 🔥 SIMPAN KE DB
        if session:
            create(session, {
                "session_id": "user_1",
                "question": query,
                "answer": answer,
                "context": context
            })

        return {
            "query": query,
            "answer": answer
        }

