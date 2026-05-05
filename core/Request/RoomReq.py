from pydantic import BaseModel

class RoomRequest(BaseModel): 
    user_id: str
    title : str 