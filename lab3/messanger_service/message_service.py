from typing import List
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Response, HTTPException

from models import Message

app = FastAPI()
chat_dict = {'Tech Sup' : [Message(content='first', sender_login='m', chat_name='Tech Sup', sending_date=datetime(2024,12,5)), Message(content='second', sender_login='m', chat_name='Tech Sup', sending_date=datetime(2024,12,6))]}


@app.post('/send', summary='Send message', response_class=Response)
async def send_message(message: Message):
    message.sending_date = datetime.now()
    if message.chat_name in chat_dict.keys():
        chat_dict[message.chat_name].append(message)
    else:
        chat_dict[message.chat_name] = [message]
        # chat_dict[message.chat_name].append(message)
    return Response(status_code=200)


@app.get('/history', summary='Get all messages by chat', response_model=List[Message])
async def get_all_messages_by_chat(chat_name: str):
    for _, chat in enumerate(chat_dict):
        if chat == chat_name:
            return chat_dict[chat]
    raise HTTPException(status_code=404, detail="Chat not found")


@app.post('/create', summary='Create new chat', response_model=str)
async def create_chat(chat: str):
    for _, exist_chat in enumerate(chat_dict):
        if exist_chat == chat:
            raise HTTPException(status_code=404, detail="Chat already exist")
    chat_dict[chat] = []
    return chat


@app.get('/chat_list', summary='Get all chats', response_model=List[str])
async def get_all_chats():
    return chat_dict.keys()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0")