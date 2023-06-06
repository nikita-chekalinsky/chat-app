import asyncio
from logging import Logger
from . import (
    AioRmqConsumer,
    AsyncServer,
    ClientsSender,
)


class MainServerLoop:

    def __init__(self,
                 async_server: AsyncServer,
                 aio_rmq_consumer: AioRmqConsumer,
                 clients_sender: ClientsSender,
                 logger: Logger):
        self.name: str = 'MainServerLoop'
        self._logger: Logger = logger

        self._async_server: AsyncServer = async_server
        self._aio_rmq_consumer: AioRmqConsumer = aio_rmq_consumer
        self._clients_sender: ClientsSender = clients_sender

        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()

        self._main_task: asyncio.Task = self._loop.create_task(self.main(),
                                                               name='Main-Task')

        self._tasks = [
            self._loop.create_task(
                self._async_server.run(), name='Async-Server-Task'),
            self._loop.create_task(
                self._aio_rmq_consumer.consume(), name='Transport-Consume-Task'),
            self._loop.create_task(
                self._clients_sender.queue_handler(), name='Clients-Sender-Task'),
        ]

    def run(self):
        self._loop.run_until_complete(self._main_task)

    def stop(self):
        self._loop.close()

    def cancel(self):
        self._main_task.cancel()

    async def _cancel_tasks(self):
        self._async_server.stop()

        for task in self._tasks:
            if not task.done():
                task.cancel()
                await task

    async def main(self):
        self._logger.warning(f'{self.name} Started')

        try:
            await asyncio.wait(self._tasks)

        except asyncio.CancelledError:
            await self._cancel_tasks()
            self._logger.warning(f'{self.name} Cancelled')

        finally:
            self._logger.warning(f'{self.name} Stopped')
