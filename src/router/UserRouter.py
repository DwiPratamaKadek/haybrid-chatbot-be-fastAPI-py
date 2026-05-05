from fastapi import APIRouter,Depends
from src.controller.UserController import UserController
from sqlmodel import Session
from db.session import get_session
from core.Request.UserReq import UserRequest

router = APIRouter()
user = UserController()

@router.post("/user")
def chat(req:UserRequest, session:Session = Depends(get_session)):
    result = user.create_user(req, session=session)
    return result

@router.get("/user")
def getHistory(session:Session = Depends(get_session)):
    result = user.get_all_user(session)
    return result