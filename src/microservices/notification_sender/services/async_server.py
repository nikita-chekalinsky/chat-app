import websockets
from logging import Logger
from typing import Callable, Coroutine
from websockets.server import WebSocketServerProtocol


class AsyncServer:

    def __init__(self,
                 ws_handler: Callable[[WebSocketServerProtocol, str], Coroutine],
                 host: str,
                 port: int,
                 logger: Logger):
        self.name = 'AsyncWSS'
        self._logger = logger
        self._host = host
        self._port = port
        self._future_inst = websockets.serve(ws_handler=ws_handler,
                                             host=self._host,
                                             port=self._port)

        self._running_inst = None

    async def run(self):
        self._running_inst = await self._future_inst
        self._logger.warning(f'{self.name} Started '
                             f'[HOST: {self._host} PORT: {self._port}]')

    def stop(self):
        if self._running_inst and self._running_inst.is_serving():
            self._running_inst.close()
            self._logger.warning(f'{self.name} Stopped')
        else:
            self._logger.warning(f'{self.name} Already Stopped')
