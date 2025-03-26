from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    content: Optional[str] = ''
    sender_login: str 
    chat_name: str
    sending_date: datetime