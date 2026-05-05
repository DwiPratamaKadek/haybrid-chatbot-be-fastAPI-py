from src.service.RoomService import RoomService
from core.Request.RoomReq import RoomRequest

class RoomController: 
    
    def __init__(self):
        self.service = RoomService()

    def create_room(self, req:RoomRequest, session): 
        try: 
            result = self.service.create_room(req, session)
            return{
                "status" : "error",
                "data" : result
            }
        except Exception as e: 
            return{
                "status" : "error",
                "data" : str(e)
            }
        
    def get_all_room(self, session):
        try: 
            result = self.service.get_all_room(session)
            return{
                "status" : "error",
                "data" : result
            }
        except Exception as e: 
            return{
                "status" : "error",
                "data" : str(e)
            }