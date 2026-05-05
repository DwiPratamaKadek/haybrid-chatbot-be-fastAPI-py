# create table 
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class User(SQLModel, table=True): 
    id: UUID = Field(default_factory=uuid4, primary_key=True) 
    name: str 
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ChatSession(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key = "user.id")
    title: str
    create_at: datetime = Field(default_factory=datetime.utcnow)

class ChatHistory(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True) 
    user_id: UUID = Field(foreign_key = "user.id")
    session_id: UUID = Field(foreign_key="chatsession.id")
    message: str
    role: str
    create_at: datetime = Field(default_factory=datetime.utcnow)
