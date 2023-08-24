from app.settings import settings
from app.services.db.user_table_scylladb import UserTable


user_table = UserTable(
    db_password=settings.db_password,
    db_username=settings.db_username,
    keyspace=settings.db_keyspace,
)


async def on_startup():
    user_table.connect()


async def on_shutdown():
    user_table.disconnect()
