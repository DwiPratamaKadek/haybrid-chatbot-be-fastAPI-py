from sqlmodel import Session, select
from schema.chat_history import ChatSession 

def create(session: Session, data: dict):
    room = ChatSession(**data)
    session.add(room)
    session.commit()
    session.refresh(room)
    return 

def getAll(session: Session ): 
    return session.exec(select(ChatSession)).all()