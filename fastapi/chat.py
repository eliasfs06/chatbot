import requests 
import json
import httpx

from fastapi import APIRouter, HTTPException
from typing import Dict, List
from model import Message, ChatCompletion, ChatGenerate, ChatMessage
from settings import settings

users_conversations: Dict[str, List[Message]] = {}

router = APIRouter()

OLLAMA_API_CHAT_URL = settings.ollama_api_chat_url
MODEL = settings.model
STREAM = settings.stream

@router.post("/api/chat/")
async def chat(chatMessage: ChatMessage):
    user_conversation = users_conversations.get(chatMessage.user_id, [])
    user_conversation.append(Message(role="user", content=chatMessage.prompt))

    chatCompletion = ChatCompletion(
        model=MODEL, 
        stream=STREAM, 
        messages=[msg.model_dump() for msg in user_conversation]
    )

    try:
        response = requests.post(OLLAMA_API_CHAT_URL, 
                                 headers={ "Content-Type": "application/json" }, 
                                 data=json.dumps(chatCompletion.model_dump()))
        
        response.raise_for_status()

        bot_response = response.json().get("message", {}).get("content", "I'm not sure how to respond to that.")

        user_conversation.append(Message(role="assistant", content=bot_response))
        users_conversations[chatMessage.user_id] = user_conversation

        return user_conversation

    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")

@router.post("/api/generate")
async def generate_text(chatGenerate: ChatGenerate):
    try:
        payload = {
            "model": chatGenerate.model,
            "prompt": chatGenerate.prompt,
            "stream": chatGenerate.stream
        }
        response = requests.post(OLLAMA_API_CHAT_URL, 
                                 headers={ "Content-Type": "application/json" }, 
                                 data=json.dumps(payload))
        response.raise_for_status()
        return {"data": response.json()}

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with Ollama: {str(e)}")

