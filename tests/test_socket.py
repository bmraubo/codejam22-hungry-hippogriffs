from mocks.socket_wrapper_mock import SocketWrapperMock

test_requests ={
    "sign_up": r'{"user_name": "funky_goblin"}'
}

def test_socket_can_process_accepted_connection_into_JSON_object():
    socket = SocketWrapperMock(test_requests["sign_up"])
    socket.wait_for_connection()

    expected_JSON = {
        "user_name": "funky_goblin"
    }

    assert socket.parsed_request == expected_JSON

