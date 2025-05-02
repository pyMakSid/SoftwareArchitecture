from uuid import UUID

from datetime import datetime

from pydantic import BaseModel, Field, StrictStr

class Message(BaseModel):
    sender_login: str
    chat_id: UUID
    text: StrictStr = Field(min_length=1)

class Message_ID(Message):
    sending_date: datetime
    message_id: StrictStr
