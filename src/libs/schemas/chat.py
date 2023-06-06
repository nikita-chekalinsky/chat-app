from pydantic import BaseModel


class ChatCreate(BaseModel):
    name: str = None
    chat_picture_link: str = None
    user_ids: list[str] = []


class Chat(ChatCreate):
    chat_id: str


class ChatAddUsers(BaseModel):
    chat_id: str
    user_ids: list[str] = []
