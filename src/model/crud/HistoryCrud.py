from sqlmodel import Session, select
from schema.chat_history import ChatHistory

def create(session: Session, data:dict):
    history = ChatHistory(**data)
    session.add(history)
    session.commit()
    session.refresh(history)
    return history

def getAll(session: Session ): 
    return session.exec(select(ChatHistory)).all()

def getById(session: Session, id: int): 
    return session.get(ChatHistory, id)

def update(session: Session, id: int, data: dict): 
    history = session.get(ChatHistory, id)

    if not history: 
        return None
    for key, value in data.items():
        setattr(history, key, value)

    session.add(history)
    session.commit()
    session.refresh(history)

    return history

def delete(session: Session, id: int):
    history = session.get(ChatHistory, id)

    if not history: 
        return None
    
    session.delete(history)
    session.commit()

    return True
