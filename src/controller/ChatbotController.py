from src.service.rag_service import RAGhybrid

class ChatbotController:
    def __init__(self):
        self.service = RAGhybrid()

    def handle_chat(self, query:str, session):
        try:
            result = self.service.chat(query, session)
            return {
                "status" : "success",
                "data" : result
            }
        except Exception as e:
            return{
                "status" : "error",
                "data" : str(e)
            }