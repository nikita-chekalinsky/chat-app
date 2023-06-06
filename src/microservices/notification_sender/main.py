import asyncio
from libs.utils.logger import logger
from services import (
    MainServerLoop,
    AsyncServer,
    AsyncServerHandler,
    AioRmqConsumer,
    ClientsController,
    ClientsSender,
)
from settings import settings


received_messages_queue = asyncio.Queue()
clients_controller = ClientsController()

async_server_handler = AsyncServerHandler(
    logger=logger,
    clients_controller=clients_controller,
)

async_server = AsyncServer(
    ws_handler=async_server_handler.do_action,
    host=settings.http_host,
    port=settings.http_port,
    logger=logger,
)


aio_rmq_consumer = AioRmqConsumer(
    rmq_host=settings.rmq_host,
    rmq_port=settings.rmq_port,
    exchange_name='WS_EXCHANGE',
    queue_name=settings.rmq_queue_name,
    received_messages_queue=received_messages_queue,
    logger=logger,
)

clients_sender = ClientsSender(
    from_queue=received_messages_queue,
    clients_controller=clients_controller,
    logger=logger,
)

server_loop = MainServerLoop(
    async_server=async_server,
    aio_rmq_consumer=aio_rmq_consumer,
    clients_sender=clients_sender,
    logger=logger,
)

try:
    logger.info(f'Start notification sender with id {settings.rmq_queue_name}')
    server_loop.run()
except KeyboardInterrupt:
    server_loop.cancel()
    server_loop.run()
finally:
    server_loop.stop()
