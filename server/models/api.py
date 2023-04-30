from typing import List
from pydantic import BaseModel

class Message(BaseModel):
    type: str
    text: str

class Input(BaseModel):
    query: str
    history: List[Message] = []

class Output(BaseModel):
    text: str

class Conversation(BaseModel):
    id: str
    messages: List[Message] = []