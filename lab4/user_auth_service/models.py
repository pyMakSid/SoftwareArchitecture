from typing import Optional

from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Index, Integer, String


class Base(DeclarativeBase):
    pass


class DB_User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    __table_args__ = (Index('user_index', 'login', 'name'),)


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