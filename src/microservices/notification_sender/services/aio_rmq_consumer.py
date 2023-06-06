import aio_pika
import asyncio
import json
from logging import Logger


class AioRmqConsumer:

    def __init__(self,
                 rmq_host: str,
                 rmq_port: int,
                 exchange_name: str,
                 queue_name: str,
                 received_messages_queue: asyncio.Queue,
                 logger: Logger):
        self.name = 'AIO_RMQ_Consumer'
        self._logger = logger
        self._received_messages_queue = received_messages_queue
        self._rmq_host = rmq_host
        self._rmq_port = rmq_port
        self._exchange_name = exchange_name
        self._queue_name = queue_name
        self._no_ack = False
        self._conn = None
        self._channel = None
        self._exchange = None
        self._queue = None

    async def _process_message(self, body: bytes):
        message_json = json.loads(body)
        self._logger.debug(f'{self.name} Received Message: {message_json}')
        await self._received_messages_queue.put(message_json)

    async def _message_handler(self, message: aio_pika.abc.AbstractIncomingMessage):
        async with message.process(ignore_processed=True):
            try:
                await self._process_message(message.body)
                await message.ack()
            except Exception as ex:
                self._logger.error(f'{self.name} Error: {ex}')
                await message.reject()

    async def _close_conn(self):
        if self._conn:
            await self._conn.close()
            self._logger.info(f'{self.name} Connection Closed')

    async def _connect(self) -> bool:
        try:
            self._conn = await aio_pika.connect_robust(host=self._rmq_host, port=self._rmq_port)
            self._channel = await self._conn.channel()
            self._queue = await self._channel.declare_queue(self._queue_name)

            self._logger.info(f'{self.name} Connection Established')

            await self._queue.consume(callback=self._message_handler, no_ack=self._no_ack)

            return True

        except asyncio.CancelledError:
            await self._close_conn()
            self._logger.warning(f'{self.name} Stopped')
            return False

        except Exception as ex:
            await self._close_conn()
            return False

    async def consume(self):
        if not await self._connect():
            return
        try:
            self._logger.warning(f'{self.name} Started')
            await asyncio.Future()

        except asyncio.CancelledError as ex:
            await self._close_conn()
            self._logger.warning(f'{self.name} Stopped')

        except Exception as ex:
            await self._close_conn()
            self._logger.error(f'{self.name} Stopped {ex}')
