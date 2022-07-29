from src.models import (
    ChatRoomModel,
    ChatRoomResponseModel,
    MessageModel,
    SendMessageResponseModel,
    SignUpResponseModel,
    UserModel,
)


class ResponseFactory:
    """This class generates responses"""

    @staticmethod
    def generate_sign_up_response(
        status: bool, user_model: UserModel, chat_room_model: ChatRoomModel
    ) -> dict:
        """Generates sign up response in JSON"""
        response_model = SignUpResponseModel(
            status=status, user=user_model, chat_room=chat_room_model
        )
        return response_model.dict()

    @staticmethod
    def generate_send_message_response(status: bool, message: MessageModel) -> dict:
        """Generates send_message response in JSON"""
        response_model = SendMessageResponseModel(status=status, message=message)
        return response_model.dict()

    @staticmethod
    def generate_get_messages_response(
        chatroom: ChatRoomModel, messages: [MessageModel]
    ) -> dict:
        """Generates get_messages response in JSON"""
        response_model = ChatRoomResponseModel(
            chat_room_id=chatroom.chat_room_id, messages=messages
        )
        return response_model.dict()
