from pydantic import BaseModel, Field

class UserRequest(BaseModel): 
    name: str
    password : str

class UserLogin(BaseModel):
    name: str
    password: str = Field(min_length=6, max_length=72)