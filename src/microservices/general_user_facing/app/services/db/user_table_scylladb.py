from uuid import UUID
from app.services.db.user_table_interface import IUserTable
from libs.scylladb import ScyllaDB
from libs.schemas.user import (
    User,
    UserAddChats,
    UserUpdate,
)


class UserTable(ScyllaDB, IUserTable):
    def connect(self) -> None:
        super().connect()
        self.prepared_statements = {
            'get_user': self.session.prepare(
                'SELECT * FROM users WHERE user_id = ?'
            ),
            'create_user': self.session.prepare(
                'INSERT INTO users (user_id, username, chat_ids) VALUES (?, ?, ?)'
            ),
            'update_user': self.session.prepare(
                'UPDATE users SET username = ? WHERE user_id = ?'
            ),
            'add_chats': self.session.prepare(
                'UPDATE users SET chat_ids = chat_ids + ? WHERE user_id = ?'
            ),
            'delete_user': self.session.prepare(
                'DELETE FROM users WHERE user_id = ?'
            ),
            'get_users': self.session.prepare(
                'SELECT user_id, username, chat_ids FROM users WHERE user_id IN ?'
            )
        }

    def get_user(self, user_id: UUID) -> User | None:
        result = self.session.execute(
            self.prepared_statements['get_user'],
            (user_id,),
        )
        return User(**result[0]) if result else None

    def create_user(self, user: User) -> User:
        self.session.execute(
            self.prepared_statements['create_user'],
            (user.user_id, user.username, user.chat_ids),
        )
        return user

    def update_user(self, user: UserUpdate) -> UserUpdate:
        self.session.execute(
            self.prepared_statements['update_user'],
            (user.username, user.user_id),
        )
        return user

    def add_chats(self, user_chats: UserAddChats) -> UserAddChats:
        self.session.execute(
            self.prepared_statements['add_chats'],
            (user_chats.chat_ids, user_chats.user_id),
        )
        return user_chats

    def delete_user(self, user_id: UUID) -> None:
        self.session.execute(
            self.prepared_statements['delete_user'],
            (user_id,),
        )

    def get_users(self, user_ids: list[UUID]) -> list[User]:
        result = self.session.execute(
            self.prepared_statements['get_users'],
            (user_ids,),
        )
        return [User(**user) for user in result]
