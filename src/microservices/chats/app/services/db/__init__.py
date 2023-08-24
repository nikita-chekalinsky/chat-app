from app.settings import settings
from app.services.db.chat_table_scylladb import ChatTable
from app.services.db.message_table_scylladb import MessageTable

chat_table = ChatTable(
    db_password=settings.db_password,
    db_username=settings.db_username,
    keyspace=settings.db_keyspace,
)
message_table = MessageTable(
    db_password=settings.db_password,
    db_username=settings.db_username,
    keyspace=settings.db_keyspace,
)


async def on_startup():
    chat_table.connect()
    message_table.connect()


async def on_shutdown():
    chat_table.disconnect()
    message_table.disconnect()
