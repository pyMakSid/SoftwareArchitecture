from typing import Optional

from passlib.context import CryptContext
from pydantic import BaseModel


class User(BaseModel):
    login : str
    password : str
    name : Optional[str] = None


class Password:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(password: str):
        return Password.pwd_context.hash(password)
    
    def verify_password(inp_password: str, hashed_password: str):
        return Password.pwd_context.verify(inp_password, hashed_password)
    