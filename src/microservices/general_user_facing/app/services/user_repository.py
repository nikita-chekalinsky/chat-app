from uuid import UUID, uuid4
from fastapi import Request
from libs.schemas.user import (
    User,
    UserCreate,
    UserUpdate,
    UserAddChats,
)
from app.services.db import user_table


class UserRepository:

    async def get_user(self,
                       request: Request,
                       user_id: UUID) -> User:
        return user_table.get_user(user_id)

    async def create_user(self, user: UserCreate) -> User:
        user_new = User(
            user_id=uuid4(),
            username=user.username,
            chat_ids=user.chat_ids,
        )
        return user_table.create_user(user_new)

    async def update_user(self, user: UserUpdate) -> User:
        user_table.update_user(user)
        return user_table.get_user(user.user_id)

    async def add_chats(self, user_chats: UserAddChats) -> User:
        user_table.add_chats(user_chats)
        return user_table.get_user(user_chats.user_id)

    async def delete_user(self, user_id: UUID) -> None:
        return user_table.delete_user(user_id)

    async def get_users(self, user_ids: list[UUID]) -> list[User]:
        return user_table.get_users(user_ids)
