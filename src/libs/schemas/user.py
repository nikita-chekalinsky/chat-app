from uuid import UUID
from pydantic import BaseModel


class UserUpdate(BaseModel):
    user_id: UUID
    username: str = ''


class UserCreate(BaseModel):
    username: str = ''
    chat_ids: set[UUID] = set()


class User(UserCreate):
    user_id: UUID


class UserAddChats(BaseModel):
    user_id: UUID
    chat_ids: set[UUID] = set()
