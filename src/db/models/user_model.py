from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.orm import relationship

from ..session import Base
from .messages_model import Message


class User(Base):
    """User Table Definition"""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, unique=True)
    name = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    children_2 = relationship(Message)
    user_one_rel = relationship("ChatRoom", foreign_keys="ChatRoom.user_one")
    user_two_rel = relationship("ChatRoom", foreign_keys="ChatRoom.user_two")

    def __repr__(self):
        return "<User(name='{}', chat_room_id='{}')>".format(
            self.name, self.chat_room_id
        )
