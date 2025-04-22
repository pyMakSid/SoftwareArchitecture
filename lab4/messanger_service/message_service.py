from uuid import UUID
from datetime import datetime

import uvicorn
from pymongo import mongo_client
from fastapi import FastAPI, HTTPException

from models import Message

app = FastAPI()

client = mongo_client.MongoClient(host='mongo', port=27017, uuidRepresentation='standard')
messages = client['messenger']['messages']

@app.post('/send', summary='Send message', response_model=Message)
async def send_message(message: Message):
    result = messages.insert_one(message.model_dump())
    return Message(**message.model_dump(),date=datetime.now(), message_id=str(result.inserted_id))


@app.get('/chat_history', summary='Get chat messages', response_model=list[Message])
async def get_chat_history(chat_id: UUID = None):
    if chat_id:
        return list(messages.find({'chat_id': {'$eq': chat_id}}))
    raise HTTPException(status_code=404, detail="Chat not found")


@app.get('/user_history', summary='Get user messages', response_model=list[Message])
async def get_user_history(user_login: str = None):
    if user_login:
        return list(messages.find({'sender_login': {'$eq': user_login}}))
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0")