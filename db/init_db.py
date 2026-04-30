from sqlmodel import SQLModel
from db.connection import engine
from schema.chat_history import ChatHistory

def init_db():
    SQLModel.metadata.create_all(engine)
