from pydantic import BaseModel
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from src.db.models.chat_room_model import ChatRoom
from src.db.models.messages_model import Message
from src.db.models.user_model import User

UserModel = sqlalchemy_to_pydantic(User)
MessageModel = sqlalchemy_to_pydantic(Message)
ChatRoomModel = sqlalchemy_to_pydantic(ChatRoom)


# Response Models
class SignUpResponseModel(BaseModel):
    """Sign Up Response Model"""

    status: bool
    user: UserModel


class SendMessageResponseModel(BaseModel):
    """Send Message Response Model"""

    status: bool
    message: MessageModel


class ChatRoomResponseModel(BaseModel):
    """Get Messages Response Model"""

    chat_room_id: str
    messages: list[MessageModel]
