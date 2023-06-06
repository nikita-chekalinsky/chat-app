from fastapi import HTTPException
from aiodynamo.client import Client
from aiodynamo.credentials import Key, StaticCredentials
from aiodynamo.http.aiohttp import AIOHTTP
from aiohttp import ClientSession
from libs.utils.logger import logger


class DynamoDBService:
    status_codes = {}
    tables = {}
    db: Client = None
    _http_client = None

    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 region: str):
        self.access_key = access_key
        self.secret_key = secret_key
        self.region = region

    def db_connect(self) -> tuple[Client, ClientSession]:
        if not DynamoDBService._http_client:
            logger.info('Creating http client')
            DynamoDBService._http_client = ClientSession()

        if not DynamoDBService.db:
            logger.info('Connecting to dynamodb')
            DynamoDBService.db = Client(
                AIOHTTP(DynamoDBService._http_client),
                StaticCredentials(
                    Key(id=self.access_key,
                        secret=self.secret_key
                        )),
                self.region
            )
        return DynamoDBService.db, DynamoDBService._http_client

    async def db_disconnect(self):
        logger.info('Disconnecting from dynamodb')
        if DynamoDBService._http_client:
            logger.info('Closing http client')
            await DynamoDBService._http_client.close()
            DynamoDBService._http_client = None
            DynamoDBService.db = None

    @staticmethod
    def error_handler(method):
        async def inner(self: DynamoDBService, *args, **kwargs):
            try:
                response = await method(self, *args, **kwargs)
                return response
            except Exception as err:
                if (status := self.status_codes.get(type(err), None)):
                    raise HTTPException(
                        status_code=status,
                        detail=str(err)
                    )
                logger.error(f"{type(err)} :: {err}")
                raise HTTPException(
                    status_code=500, detail=str(type(err)))
        return inner
