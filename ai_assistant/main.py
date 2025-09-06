from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from services.mistral import ask_mistral  # ta fonction existante

app = FastAPI()

# Autoriser ton frontend (ajuste l'URL si nécessaire)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Reçoit un message et retourne la réponse du modèle Mistral"""
    reply = ask_mistral(request.message)
    return {"reply": reply}
