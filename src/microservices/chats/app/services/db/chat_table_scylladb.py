from uuid import UUID
from app.services.db.chat_table_interface import IChatTable
from libs.scylladb import ScyllaDB
from libs.schemas.chat import (
    Chat,
    ChatAddUsers,
)


class ChatTable(ScyllaDB, IChatTable):
    def connect(self) -> None:
        super().connect()
        self.prepared_statements = {
            "get_chat": self.session.prepare(
                "SELECT chat_id, name, user_ids FROM chats WHERE chat_id = ?"
            ),
            "create_chat": self.session.prepare(
                "INSERT INTO chats (chat_id, name, user_ids) VALUES (?, ?, ?)"
            ),
            "add_users_to_chat": self.session.prepare(
                "UPDATE chats SET user_ids = user_ids + ? WHERE chat_id = ?"
            ),
            "remove_users_from_chat": self.session.prepare(
                "UPDATE chats SET user_ids = user_ids - ? WHERE chat_id = ?"
            ),
        }

    def get_chat(self, chat_id: UUID) -> Chat | None:
        result = self.session.execute(
            self.prepared_statements["get_chat"],
            (chat_id,)
        )
        return Chat(**result[0]) if result else None

    def create_chat(self, chat: Chat) -> Chat:
        self.session.execute(
            self.prepared_statements["create_chat"],
            (chat.chat_id, chat.name, chat.user_ids)
        )
        return chat

    def add_users_to_chat(self, chat_users: ChatAddUsers) -> bool:
        self.session.execute(
            self.prepared_statements["add_users_to_chat"],
            (chat_users.user_ids, chat_users.chat_id)
        )
        return True

    def remove_users_from_chat(self, chat_users: ChatAddUsers) -> bool:
        self.session.execute(
            self.prepared_statements["remove_users_from_chat"],
            (chat_users.user_ids, chat_users.chat_id)
        )
        return True
