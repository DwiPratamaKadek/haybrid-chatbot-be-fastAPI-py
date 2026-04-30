from pydantic import BaseModel

class ChabotRespond(BaseModel):
    query : str
    answare : str