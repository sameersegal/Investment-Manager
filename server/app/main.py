from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.api import Input, Conversation, Message
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/conversations", response_model=List[Conversation])
async def conversations():
    return [{"id": 1234, "messages": []}]

@app.post("/conversations", response_model=Conversation)
async def new_conversation(message: Message):
    return {"id": 1234, "messages": []}

@app.get("/conversations/:id", response_model=Conversation)
async def conversation(id: int):
    return {"id": 1234, "messages": []}

@app.post("/conversations/:id", response_model=Message)
async def response(message: Message, id: int):
    return {"message": "Hello World"}