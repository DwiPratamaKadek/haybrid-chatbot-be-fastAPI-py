from src.model.crud.RoomCrud import create, getAll
from core.Request.RoomReq import RoomRequest

class RoomService: 
    
    def create_room(self, req: RoomRequest, session=None):
        if session: 
            data = create(session, {
                "user_id" : req.user_id,
                "title" : req.title,  
            })
        
        return data

    def get_all_room(self, session=None):
        return getAll(session)