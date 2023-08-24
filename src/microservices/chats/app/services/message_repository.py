from datetime import datetime
from fastapi import Request
from uuid import UUID
from libs.schemas.message import (
    Message,
)
from app.services.db import message_table


class MessageRepository:

    async def get_message(self,
                          request: Request,
                          chat_id: UUID,
                          message_timestamp: datetime) -> list[Message]:
        return message_table.get_message(chat_id, message_timestamp)

    async def get_messages(self,
                           request: Request,
                           chat_id: UUID,
                           start_timestamp: datetime | None,
                           end_timestamp: datetime | None) -> list[Message]:
        return message_table.get_messages(chat_id, start_timestamp, end_timestamp)

    async def create_message(self,
                             request: Request,
                             message: Message) -> Message:
        return message_table.create_message(message)
