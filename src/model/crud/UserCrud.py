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


def getByName(session:Session, name:str): 
    user = session.exec(
        select(User).where(User.name == name)
    ).first()

    return user
