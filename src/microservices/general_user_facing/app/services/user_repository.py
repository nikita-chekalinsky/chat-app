from uuid import uuid4
from fastapi import Request
from aiodynamo.errors import ItemNotFound
from aiodynamo.expressions import F
from aiodynamo.models import ReturnValues
from libs.schemas.user import (
    User,
    UserPublic,
    UserCreate,
    UserUpdate,
    UserAddChats,
)
from app.services.db_init import dynamodb as db


class UserRepository:

    def __init__(self):
        self.status_codes = {
            ItemNotFound: 204,
        }
        self.db, _ = db.db_connect()
        self.tables = {
            'users': self.db.table('users')
        }

    @db.error_handler
    async def get_user(self,
                       request: Request, user_id: str) -> User:
        response = await self.tables['users'].get_item({'user_id': user_id})
        return User(**response)

    @db.error_handler
    async def create_user(self, user: UserCreate) -> User:
        user_new = {
            **user.dict(),
            'user_id': str(uuid4()),
            'chat_ids': []
        }
        await self.tables['users'].put_item(user_new)
        return User(**user_new)

    @db.error_handler
    async def update_user(self, user: UserUpdate) -> User:
        update_expression = (
            F('username').set(user.username) &
            F('profile_picture_link').set(user.profile_picture_link)
        )
        user = await self.tables['users'].update_item(
            key={'user_id': user.user_id},
            update_expression=update_expression,
            return_values=ReturnValues('ALL_NEW'),
            condition=F('user_id').exists(),
        )
        return User(**user)

    @db.error_handler
    async def add_chat(self, user_chats: UserAddChats) -> User:
        user = await self.tables['users'].update_item(
            key={'user_id': user_chats.user_id},
            update_expression=F('chat_ids').append(user_chats.chat_ids),
            return_values=ReturnValues('ALL_NEW'),
            condition=F('user_id').exists(),
        )
        return User(**user)

    async def delete_user(self, user_id: str) -> None:
        raise NotImplementedError

    async def get_users(self, user_ids: list[str]) -> list[UserPublic]:
        raise NotImplementedError
