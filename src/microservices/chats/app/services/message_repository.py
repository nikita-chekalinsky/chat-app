from datetime import datetime
from fastapi import Request
from aiodynamo.errors import ItemNotFound
from aiodynamo.expressions import HashKey, RangeKey
from libs.schemas.message import (
    Message,
)
from app.services.db_init import dynamodb as db


class MessageRepository:
    __none_type = type(None)
    __range_key_from_timestamp = {
        (datetime, __none_type): lambda x, y: RangeKey('message_timestamp').gte(x),
        (__none_type, datetime): lambda x, y: RangeKey('message_timestamp').lte(y),
        (datetime, datetime): lambda x, y: RangeKey('message_timestamp').between(x, y),
        (__none_type, __none_type): lambda x, y: None,
    }

    def __init__(self):
        self.status_codes = {
            ItemNotFound: 204,
        }
        self.db, _ = db.db_connect()
        self.tables = {
            'chats': self.db.table('chats'),
            'messages': self.db.table('messages'),
        }

    @db.error_handler
    async def get_message(self,
                          request: Request,
                          chat_id: str,
                          message_timestamp: datetime) -> list[Message]:
        response = await self.tables['messages'].get_item({
            'chat_id': chat_id,
            'message_timestamp': str(message_timestamp)})
        return [Message(**response)]

    @db.error_handler
    async def get_messages(self,
                           request: Request,
                           chat_id: str,
                           start_timestamp: datetime | None,
                           end_timestamp: datetime | None) -> list[Message]:
        timestamps = (type(start_timestamp), type(end_timestamp))
        range_key = self.__range_key_from_timestamp[timestamps](
            str(start_timestamp),
            str(end_timestamp),
        )
        if range_key:
            key_condition = HashKey('chat_id', chat_id) & range_key
        else:
            key_condition = HashKey('chat_id', chat_id)
        return [Message(**item) async for item in
                self.tables['messages'].query(key_condition)]

    @db.error_handler
    async def create_message(self,
                             request: Request,
                             message: Message) -> Message:
        message_new = message.dict()
        message_new['message_timestamp'] = str(message.message_timestamp)
        await self.tables['messages'].put_item(message_new)
        return message
