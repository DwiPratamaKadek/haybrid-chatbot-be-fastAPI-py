from fastapi import APIRouter,Depends
from src.controller.ChatbotController import ChatbotController
from sqlmodel import Session
from db.session import get_session
from core.Request.ChabotReq import ChabotRequest



router = APIRouter()
chatbot = ChatbotController()

@router.post("/chat")
def chat(req:ChabotRequest, session:Session = Depends(get_session)):
    result = chatbot.handle_chat(req.query, session=session)
    return result