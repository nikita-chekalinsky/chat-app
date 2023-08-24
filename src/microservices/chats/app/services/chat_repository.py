from uuid import uuid4, UUID
from fastapi import Request
from libs.schemas.chat import (
    Chat,
    ChatCreate,
    ChatAddUsers,
)
from app.services.db import chat_table


class ChatRepository:

    async def get_chat(self,
                       request: Request,
                       chat_id: UUID) -> Chat | None:
        return chat_table.get_chat(chat_id)

    async def create_chat(self,
                          request: Request,
                          chat: ChatCreate) -> Chat:
        chat_new = Chat(
            chat_id=uuid4(),
            **chat.model_dump(),
        )
        chat_table.create_chat(chat_new)
        return chat_new

    async def add_users_to_chat(self,
                                request: Request,
                                chat_users: ChatAddUsers) -> Chat:
        chat = chat_table.get_chat(chat_users.chat_id)
        chat_table.add_users_to_chat(chat_users)
        return Chat(name=chat.name,
                    user_ids=chat.user_ids | chat_users.user_ids,
                    chat_id=chat.chat_id,)

    async def remove_users_from_chat(self,
                                     request: Request,
                                     chat_users: ChatAddUsers) -> Chat:
        chat = chat_table.get_chat(chat_users.chat_id)
        chat_table.remove_users_from_chat(chat_users)
        return Chat(name=chat.name,
                    user_ids=chat.user_ids - chat_users.user_ids,
                    chat_id=chat.chat_id,)
