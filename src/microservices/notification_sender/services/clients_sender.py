import asyncio
import json
from logging import Logger
from .clients_controller import ClientsController
from websockets.exceptions import (
    ConnectionClosedOK as WS_ConnectionClosedOK,
    ConnectionClosedError as WS_ConnectionClosedError,
)
from websockets.server import WebSocketServerProtocol


class ClientsSender:

    def __init__(self,
                 from_queue: asyncio.Queue,
                 clients_controller: ClientsController,
                 logger: Logger):
        self.name = 'ClientsSender'
        self._from_queue = from_queue
        self._clients_controller = clients_controller
        self._logger = logger

    def _remove_disconnected_client(self, client_id: str):
        self._clients_controller.remove_client(client_id)

    async def _send_update(self, receivers: list[tuple[str, WebSocketServerProtocol]], message: dict):
        if not len(receivers):
            return

        message = json.dumps(message)

        for receiver_data in receivers:
            client_id, receiver = receiver_data

            try:
                await receiver.send(message)
                self._logger.debug(f'{self.name} S > {message}')

            except (WS_ConnectionClosedOK, WS_ConnectionClosedError) as ex:
                self._logger.debug(f'{self.name} Client [Id:{client_id}]'
                                   f' Disconnected! Reason: {str(ex)}')
                self._remove_disconnected_client(client_id)

    async def _process_received_message(self, message_json: dict):
        self._logger.debug(f'{self.name} R < {message_json}')
        client_id = message_json.get('client_id')
        if client_id:
            client = self._clients_controller.get_client(client_id)
            await self._send_update([(client_id, client)], message_json)

    async def queue_handler(self):
        self._logger.warning(f'{self.name} Started')

        try:
            while True:
                message_json = await self._from_queue.get()
                if not self._clients_controller.check_clients_exist():
                    self._from_queue.task_done()
                    continue

                await self._process_received_message(message_json)

                self._from_queue.task_done()

        except asyncio.CancelledError:
            self._logger.warning(f'{self.name} Stopped')
            return

        except Exception as ex:
            self._logger.error(f'{self.name} Stopped {ex}')
            return
