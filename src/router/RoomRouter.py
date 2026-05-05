from fastapi import APIRouter,Depends
from src.controller.RoomController import RoomController
from sqlmodel import Session
from db.session import get_session
from core.Request.RoomReq import RoomRequest

router = APIRouter()
room = RoomController()

@router.post("/room")
def chat(req:RoomRequest, session:Session = Depends(get_session)):
    result = room.create_room(req, session=session)
    return result

@router.get("/room")
def getHistory(session:Session = Depends(get_session)):
    result = room.get_all_room(session)
    return result