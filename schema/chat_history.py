# create table 
from sqlmodel import SQLModel, Field
from datetime import datetime

class ChatHistory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    session_id: str
    question: str
    answer: str
    # context: str | None = None
    # model: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

