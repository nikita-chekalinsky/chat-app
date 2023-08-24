from abc import ABC, abstractmethod
from uuid import UUID
from libs.schemas.chat import (
    Chat,
    ChatCreate,
    ChatAddUsers,
)


class IChatTable(ABC):
    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def get_chat(self, chat_id: UUID) -> Chat: ...

    @abstractmethod
    def create_chat(self, chat: ChatCreate) -> Chat: ...

    @abstractmethod
    def add_users_to_chat(self, chat_users: ChatAddUsers) -> Chat: ...
