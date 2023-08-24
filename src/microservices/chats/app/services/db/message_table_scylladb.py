from datetime import datetime
from uuid import UUID
from app.services.db.message_table_interface import IMessageTable
from libs.scylladb import ScyllaDB
from libs.schemas.message import (
    Message,
)


class MessageTable(ScyllaDB, IMessageTable):
    __none_type = type(None)
    __range_key_from_timestamp = {
        (datetime, __none_type): lambda x, y: (x,),
        (__none_type, datetime): lambda x, y: (y,),
        (datetime, datetime): lambda x, y: (x, y),
        (__none_type, __none_type): lambda x, y: tuple(),
    }

    def connect(self) -> None:
        super().connect()
        self.select_query_init = "SELECT chat_id, message_timestamp, message_text, sender_id, attachment_links FROM messages WHERE chat_id = ? "
        self.prepared_statements = {
            "get_message": self.session.prepare(
                self.select_query_init +
                "AND message_timestamp = ? BYPASS CACHE"
            ),
            "get_messages": {
                (datetime, self.__none_type): self.session.prepare(
                    self.select_query_init +
                    "AND message_timestamp >= ? BYPASS CACHE"
                ),
                (self.__none_type, datetime): self.session.prepare(
                    self.select_query_init +
                    "AND message_timestamp <= ? BYPASS CACHE"
                ),
                (datetime, datetime): self.session.prepare(
                    self.select_query_init +
                    "AND message_timestamp >= ? AND message_timestamp <= ? BYPASS CACHE"
                ),
                (self.__none_type, self.__none_type): self.session.prepare(
                    self.select_query_init
                ),
            },
            "create_message": self.session.prepare(
                "INSERT INTO messages (chat_id, message_timestamp, message_text, sender_id, attachment_links) VALUES (?, ?, ?, ?, ?)"
            ),
        }

    def get_message(self,
                    chat_id: UUID,
                    message_timestamp: datetime) -> list[Message]:
        response = self.session.execute(
            self.prepared_statements['get_message'],
            (chat_id, message_timestamp)
        )
        return [Message(**response[0])] if response else []

    def get_messages(self,
                     chat_id: UUID,
                     start_timestamp: datetime | None,
                     end_timestamp: datetime | None) -> list[Message]:
        timestamps = (type(start_timestamp), type(end_timestamp))
        range_key = self.__range_key_from_timestamp[timestamps](
            start_timestamp,
            end_timestamp,
        )
        response = self.session.execute(
            self.prepared_statements['get_messages'][timestamps],
            (chat_id, *range_key)
        )
        return [Message(**row) for row in response]

    def create_message(self, message: Message) -> Message:
        if message.message_timestamp is None:
            message.message_timestamp = datetime.now()
        self.session.execute(
            self.prepared_statements['create_message'],
            (message.chat_id,
             message.message_timestamp,
             message.message_text,
             message.sender_id,
             message.attachment_links)
        )
        return message
