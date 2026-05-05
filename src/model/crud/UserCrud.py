from sqlmodel import Session, select
from schema.chat_history import User

def create(session: Session, data:dict):
    user = User(**data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def getAll(session: Session ): 
    return session.exec(select(User)).all()

def getById(session: Session, id: int): 
    return session.get(User, id)

def update(session: Session, id: int, data: dict): 
    user = session.get(User, id)

    if not user: 
        return None
    for key, value in data.items():
        setattr(user, key, value)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def delete(session: Session, id: int):
    user = session.get(User, id)

    if not user: 
        return None
    
    session.delete(user)
    session.commit()

    return True