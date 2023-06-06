from libs.dynamodb import DynamoDBService
from app.settings import settings


dynamodb = DynamoDBService(access_key=settings.dynamodb_user_key,
                           secret_key=settings.dynamodb_user_secret,
                           region=settings.region)


async def on_startup():
    dynamodb.db_connect()


async def on_shutdown():
    await dynamodb.db_disconnect()
