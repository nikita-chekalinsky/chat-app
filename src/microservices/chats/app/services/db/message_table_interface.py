from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime
from libs.schemas.message import (
    Message,
)


class IMessageTable(ABC):
    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def get_message(self,
                    chat_id: UUID,
                    message_timestamp: datetime) -> list[Message]: ...

    @abstractmethod
    def get_messages(self,
                     chat_id: UUID,
                     start_timestamp: datetime | None,
                     end_timestamp: datetime | None) -> list[Message]: ...

    @abstractmethod
    def create_message(self, message: Message) -> Message: ...
