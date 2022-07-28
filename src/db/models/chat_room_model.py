from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from ..session import Base
from .messages_model import Message


class ChatRoom(Base):
    """Message Table Definition"""

    __tablename__ = "chatrooms"
    id = Column(Integer, primary_key=True)
    chat_room_id = Column(String, unique=True)
    user_one = Column(String, ForeignKey("users.user_id"))
    user_two = Column(String, ForeignKey("users.user_id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    message_relation_ship = relationship(Message)

    def __repr__(self):
        return "<ChatRoom(chat_room_id='{}', user_one='{}')>".format(
            self.chat_room_id, self.user_one
        )
