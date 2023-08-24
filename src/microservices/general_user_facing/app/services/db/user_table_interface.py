from abc import ABC, abstractmethod
from uuid import UUID
from libs.schemas.user import (
    User,
    UserCreate,
    UserUpdate,
    UserAddChats,
)


class IUserTable(ABC):
    @abstractmethod
    def connect(self) -> None: ...

    @abstractmethod
    def get_user(self, user_id: UUID) -> User: ...

    @abstractmethod
    def create_user(self, user: User) -> User: ...

    @abstractmethod
    def update_user(self, user: UserUpdate) -> UserUpdate: ...

    @abstractmethod
    def add_chats(self, user_chats: UserAddChats) -> UserAddChats: ...

    @abstractmethod
    def delete_user(self, user_id: UUID) -> None: ...

    @abstractmethod
    def get_users(self, user_ids: list[UUID]) -> list[User]: ...
