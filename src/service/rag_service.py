from src.model.ml.Bm25Model import Bm25Model
from src.model.ml.BgeBiEmbeddingModel import BgeBiEmbeddingModel
from src.model.ml.CrossReranking import CrossReranker
from src.model.crud.HistoryCrud import create
from src.model.crud.HistoryCrud import getAll
from src.service.GeminiService import GeminiService
from core.Request.ChabotReq import ChabotRequest

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

    def chat(self, req:ChabotRequest, session=None) : 
        # 1 BM25 
        bm25_doc = self.bm25.retrieve(req.message)
        # 2 Bi embeding 
        bi_docs = self.biEncoder.semantic_filter(
            req.message,
            bm25_doc, 
            top_k=5
        )
        # cross reranking 
        reranked_docs = self.crossRerank.rerank(
            query=req.message,
            document=bi_docs, 
            top_k=3
        )
        if not reranked_docs: 
            return{
                "query" : req.message,
                "answer" : "Informasi tidak ditemukan"
            }
        
        # Gabungkan context
        context = "\n\n".join([doc.page_content for doc in reranked_docs])
        reranked_answare = context 
      
        #prompt gemini 
        prompt = f"""
        ATURAN:
        - Jawab hanya dari konteks
        - Jika tidak ada jawaban → katakan "Tidak ditemukan dalam data"

        Konteks:
        {reranked_answare}

        Pertanyaan: {req.message}
        Jawaban:
        """

        answer = self.gemini.generate(prompt)

        # ===================== SIMPAN KE DB =========================
        
        create(session, {
            "user_id": req.user_id,
            "session_id" : req.session_id,
            "message": req.message,
            "role": "user",
        })

        create(session,{
            "user_id": req.user_id,
            "session_id" : req.session_id,
            "message": answer,
            "role": "assistant",
        })
        
        return {
            "query" : req.message, 
            "answer" : answer
        }
    
    def get_chat_per_room(self, session=None):
        return getAll(session)
        

