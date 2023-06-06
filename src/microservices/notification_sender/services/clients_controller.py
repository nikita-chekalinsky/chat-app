from websockets.server import WebSocketServerProtocol


class ClientsController:

    def __init__(self):
        self.name = 'ClientsController'
        self._clients = {}

    def check_clients_exist(self) -> bool:
        return len(self._clients) > 0

    def get_clients_amount(self) -> int:
        return len(self._clients)

    def add_client(self, client_id: str, websocket: WebSocketServerProtocol):
        self._clients[client_id] = websocket

    def remove_client(self, client_id: str):
        self._clients.pop(client_id, None)

    def get_client(self, client_id: str) -> WebSocketServerProtocol | None:
        return self._clients.get(client_id, None)
