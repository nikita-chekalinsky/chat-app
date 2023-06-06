from pydantic import BaseModel


class UserUpdate(BaseModel):
    user_id: str
    username: str = ''
    profile_picture_link: str = ''


class UserCreate(BaseModel):
    username: str = ''
    profile_picture_link: str = ''
    email: str
    password: str
    chat_ids: list[str] = []


class UserPublic(BaseModel):
    user_id: int
    username: str
    email: str
    profile_picture_link: str = None


class User(UserCreate):
    user_id: str


class UserAddChats(BaseModel):
    user_id: str
    chat_ids: list[str] = []
