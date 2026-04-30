from fastapi import FastAPI
from src.router.ChatbotRouter import router as chatbot_router
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

app.include_router(chatbot_router, prefix="/api")