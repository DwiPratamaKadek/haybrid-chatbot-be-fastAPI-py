from pydantic import BaseModel

class ChabotRequest(BaseModel):
    user_id : str
    session_id : str
    message : str