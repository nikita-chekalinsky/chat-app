import json
from logging import Logger
from .clients_controller import ClientsController
from websockets.server import WebSocketServerProtocol
from websockets.exceptions import (
    ConnectionClosedOK as WS_ConnectionClosedOK,
    ConnectionClosedError as WS_ConnectionClosedError,
)


class AsyncServerHandler:

    def __init__(self,
                 clients_controller: ClientsController,
                 logger: Logger):
        self.name = 'AsyncWSHandler'
        self._clients_controller = clients_controller
        self._logger = logger

    async def _process_data(self,
                            client_id: str,
                            websocket: WebSocketServerProtocol,
                            json_obj: dict):
        """
        This Method for specifying exchange protocol between client and server or how do server react to user requests
        :param client_id: client's uuid
        :param websocket: websocket connection with client
        :param json_obj: user's data in request
        :return: nothing (need just to send response through websocket object)
        """
        print(json_obj)

    def _parse_message(self, message: str) -> tuple[dict | None, str]:
        try:
            json_obj = json.loads(message)
        except Exception as ex:
            return None, f'Unknown message: {message}. Reason: {str(ex)}'

        return json_obj, ''

    def _add_client(self, websocket: WebSocketServerProtocol, path: str) -> str:
        client_id = path.split('/')[-1]

        self._clients_controller.add_client(client_id, websocket)
        self._logger.debug(f'{self.name} New Client [Uuid: {client_id}]')

        return client_id

    def _remove_client(self, client_id: str):
        self._clients_controller.remove_client(client_id)

        self._logger.debug(
            f'{self.name} Client Disconnected [Uuid: {client_id}]')

    async def do_action(self, websocket: WebSocketServerProtocol, path: str):
        try:
            client_id = self._add_client(websocket, path)
        except Exception as ex:
            self._logger.error(f'{self.name} Stopped {ex}')
            return

        while True:
            try:
                message = await websocket.recv()
                self._logger.debug(f'{self.name} R < {message}')

                json_obj, err = self._parse_message(message)

                if err:
                    self._logger.warning(f'{self.name} parse message: {err}')
                    continue

                await self._process_data(client_id, websocket, json_obj)

            except (WS_ConnectionClosedOK, WS_ConnectionClosedError) as ex:
                self._logger.debug(
                    f'{self.name} Client [Id:{client_id}] Disconnected! Reason: {str(ex)}')
                break

            except Exception as ex:
                self._logger.error(f'{self.name} Stopped {ex}')
                break

        try:
            self._remove_client(client_id)
        except Exception as ex:
            self._logger.error(f'{self.name} Stopped {ex}')
