import typing
import json

class SocketWrapperMock:
    parsed_request = {}

    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def wait_for_connection(self) -> str:
        self.process_connection(self.connection_string)

    def process_connection(self, request: any):
        self.parsed_request = self.parse_request(request)

    def parse_request(self, request: str) -> dict:
        return json.loads(request)
