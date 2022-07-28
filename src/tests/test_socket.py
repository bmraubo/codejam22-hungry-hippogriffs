import json

import pytest

from src.models import SignUpResponseModel, UserModel
from src.sockets.connection_handler import ConnectionHandler
from src.tests.mocks.socket_mock import SocketMock

test_requests = {"sign_up": r'{"user_name": "funky_goblin"}'}

test_user = UserModel(
    name="funky_goblin", user_id="a-user-id", chat_room_id="a-chatroom-id", id=1
)

test_responses = {"sign_up": SignUpResponseModel(status=True, user=test_user).dict()}


@pytest.mark.asyncio
async def test_socket_accepts_connection():
    """Test function to accept socket"""
    socket = SocketMock(test_requests["sign_up"])
    await socket.accept()

    assert socket.connection_accepted is True


@pytest.mark.asyncio
async def test_socket_can_process_accepted_connection_into_JSON_object():
    """Test function for socket processing"""
    socket = SocketMock(test_requests["sign_up"])
    connection_handler = ConnectionHandler(socket)
    request = await connection_handler.get_request()

    expected_JSON = {"user_name": "funky_goblin"}

    assert request == expected_JSON


@pytest.mark.asyncio
async def test_socket_can_process_JSON_objects_and_send_them_():
    """Test function for socket"""
    socket = SocketMock(json.dumps(test_responses["sign_up"]))
    connection_handler = ConnectionHandler(socket)
    await connection_handler.send_response(test_responses["sign_up"])

    expected_sent_response = (
        r'{"status": true, "user": {"id": 1, "user_id": "a-user-id", "name": "funky_goblin", '
        r'"created_at": null, "updated_at": null}}'
    )

    assert socket.sent_response == expected_sent_response
