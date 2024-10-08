from typing import Optional, List
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class User(BaseModel):
    id: str
    messages: List[Message]

class ChatMessage(BaseModel):
    user_id: int
    prompt: str

class ChatCompletion(BaseModel):
    model: str
    messages: List[Message]  
    tools: Optional[List] = None
    format: Optional[str] = None
    options: Optional[dict] = None
    stream: bool = False
    keep_alive: str = "10m"

class ChatGenerate(BaseModel):
    model: str
    prompt: str
    suffix: str = ""
    stream: bool = False
    images: Optional[List] = None
    format: Optional[str] = None
    options: Optional[dict] = None
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[str] = None
    raw: Optional[bool] = None
    keep_alive: str = "10m"
