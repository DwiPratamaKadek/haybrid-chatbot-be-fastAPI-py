from src.service.rag_service import RAGhybrid
from core.Request.ChabotReq import ChabotRequest

class ChatbotController:
    def __init__(self,):
        self.service = RAGhybrid()

    def handle_chat(self, req:ChabotRequest, session):
        try:
            result = self.service.chat(req, session)
            return {
                "status" : "success",
                "data" : result
            }
        except Exception as e:
            return{
                "status" : "error",
                "data" : str(e)
            }
    
    def handle_history(self, session):
        try: 
            data = self.service.get_chat_per_room(session)
            return{
                "status" : "success", 
                "data" : data
            }
        except Exception as e:
            return{
                "status" : "error",
                "data" : str(e)
            }
