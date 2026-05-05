from fastapi import FastAPI
from src.router.ChatbotRouter import router as chatbot_router
from src.router.UserRouter import router as user_router
from src.router.RoomRouter import router as room_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title= "Chatbot Retrieval dan Reranking",
    version="1.0"
)

origins = [
    "http://localhost:3000",  # Next.js
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pendaftaran endpoint
app.include_router(chatbot_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(room_router, prefix="/api")