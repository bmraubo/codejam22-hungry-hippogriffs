from src.models import UserModel
from src.sockets.response_factory import ResponseFactory

test_data = {
    "new_user": UserModel(
        name="funky_goblin", user_id="a-user-id", chat_room_id="a-chatroom-id", id=1
    )
}


def test_sign_up_response():
    """Test sign up response"""
    user = test_data["new_user"]
    response = ResponseFactory.generate_sign_up_response(status=True, user_model=user)

    expected_response = {
        "status": True,
        "user": {
            "id": 1,
            "chat_room_id": "a-chatroom-id",
            "name": "funky_goblin",
            "user_id": "a-user-id",
            "created_at": None,
            "updated_at": None,
        },
    }

    assert response == expected_response
