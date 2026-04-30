from pydantic import BaseModel

class ChabotRequest(BaseModel):
    query : str