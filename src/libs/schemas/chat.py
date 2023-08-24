from pydantic import BaseModel
from uuid import UUID


class ChatCreate(BaseModel):
    name: str = None
    user_ids: set[UUID] = set()


class Chat(ChatCreate):
    chat_id: UUID


class ChatAddUsers(BaseModel):
    chat_id: UUID
    user_ids: set[UUID] = set()
