from FlagEmbedding import FlagReranker

class CrossReranker:
    def __init__(self):
        self.reranker = FlagReranker(
                "BAAI/bge-reranker-large", 
                use_fp16=True
            )

    def rerank(self, query, document, top_k=3):
        pairs = [(query, doc.page_content) for doc in document]
        scores = self.reranker.compute_score(pairs)

        reranked = sorted(
            zip(document, scores), 
            key=lambda x: x[1],
            reverse=1
        )                        

        return [doc for doc, _ in reranked[:3]]