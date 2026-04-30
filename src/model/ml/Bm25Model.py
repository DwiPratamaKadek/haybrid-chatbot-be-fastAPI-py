
from langchain_core.documents import Document
from langchain_community.retrievers import BM25Retriever
from nltk.tokenize import word_tokenize

class Bm25Model:

    def __init__(self, texts, top_k = 10):
        self.top_k = top_k 

        docs = [
            Document(page_content=text)
            for text in texts if isinstance(text, str) and text.strip()

        ]

        self.retriever = BM25Retriever.from_documents(
            docs, 
            k=self.top_k, 
            preprocess_func=word_tokenize,
        ) 
    
    def retrieve(self, query):
        return self.retriever.invoke(query)