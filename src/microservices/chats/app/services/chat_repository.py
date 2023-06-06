from uuid import uuid4
from fastapi import Request
from aiodynamo.errors import ItemNotFound
from aiodynamo.expressions import F
from aiodynamo.models import ReturnValues
from libs.schemas.chat import (
    Chat,
    ChatCreate,
    ChatAddUsers,
)
from app.services.db_init import dynamodb as db


class ChatRepository:

    def __init__(self):
        self.status_codes = {
            ItemNotFound: 204,
        }
        self.db, _ = db.db_connect()
        self.tables = {
            'users': self.db.table('users'),
            'chats': self.db.table('chats')
        }

    @db.error_handler
    async def get_chat(self,
                       request: Request,
                       chat_id: str) -> Chat | None:
        response = await self.tables['chats'].get_item({'chat_id': chat_id})
        return Chat(**response)

    @db.error_handler
    async def create_chat(self,
                          request: Request,
                          chat: ChatCreate) -> Chat:
        chat_new = {
            **chat.dict(),
            "chat_id": str(uuid4()),
        }
        await self.tables['chats'].put_item(chat_new)
        return Chat(**chat_new)

    @db.error_handler
    async def add_users_to_chat(self,
                                request: Request,
                                chat_users: ChatAddUsers) -> Chat:
        chat = await self.tables['chats'].update_item(
            key={'chat_id': chat_users.chat_id},
            update_expression=F('user_ids').append(chat_users.user_ids),
            return_values=ReturnValues('ALL_NEW'),
            condition=F('chat_id').exists(),
        )
        return Chat(**chat)
