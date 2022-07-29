import datetime
import json


def default(o):
    """Date Time parser for json dumps"""
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


class ConnectionHandler:
    """Connection handler"""

    def __init__(self, socket):
        self.socket = socket

    async def get_request(self) -> dict:
        """Returns json request from client"""
        return await self.process_incoming_connection()

    async def accept_socket_connection(self):
        """Accepts connection"""
        return await self.socket.accept()

    async def send_response(self, response: dict) -> None:
        """Sends json response to the client"""
        await self.socket.send_text(json.dumps(response, default=default))

    async def process_incoming_connection(self) -> dict:
        """Recieve Messages and  returns request"""
        request = await self.socket.receive_text()
        return self.parse_request(request)

    def parse_request(self, request: str) -> dict:
        """Resquest parser"""
        return json.loads(request)
