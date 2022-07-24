import json


class ConnectionHandler:
    parsed_request = {}

    def __init__(self, socket):
        self.socket = socket

    async def get_request(self):
        return await self.wait_for_connection()

    async def send_response(self, response: dict):
        await self.socket.send_text(json.dumps(response))

    async def wait_for_connection(self) -> str:
        await self.socket.accept()
        while True:
            request = await self.socket.receive_text()
            return self.parse_request(request)

    def parse_request(self, request: str) -> dict:
        return json.loads(request)
