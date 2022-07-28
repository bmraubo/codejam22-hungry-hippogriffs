from typing import List

from src.sockets.connection_handler import ConnectionHandler


class ConnectionManager:
    """Connection Manager is needed to broadcast stuff"""

    def __init__(self):
        self.active_connections: List[ConnectionHandler] = []

    def add_connection(self, connection: ConnectionHandler):
        """Adds connection to active list"""
        self.active_connections.append(connection)

    def disconnect(self, connection: ConnectionHandler):
        """Removes connection from active list"""
        self.active_connections.remove(connection)

    async def broadcast(self, message: dict):
        """Broadcast message to all active users in chatroom"""
        for connection in self.active_connections:
            await connection.send_response(message)
