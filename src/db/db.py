from src.db.models.chat_room_model import ChatRoom
from src.db.models.messages_model import Message
from src.db.models.user_model import User
from src.db.session import Base, Session, engine
from src.models import ChatRoomModel, MessageModel, UserModel

Base.metadata.create_all(engine)


class DatabaseService:
    """User Factory Class is used to create user"""

    def save_user(self, user_obj: UserModel) -> UserModel:
        """Saves user object to database"""
        user_db_model = User(
            name=user_obj.name,
            user_id=user_obj.user_id,
        )
        Session.add(user_db_model)
        Session.commit()
        return UserModel.from_orm(user_db_model)

    def save_chat_room(self, chat_room_obj: ChatRoomModel) -> ChatRoomModel:
        """Save chatRoom"""
        chat_room_db = (
            Session.query(ChatRoom)
            .filter_by(chat_room_id=chat_room_obj.chat_room_id)
            .first()
        )
        if not chat_room_db:
            chat_room_db = ChatRoom(
                chat_room_id=chat_room_obj.chat_room_id,
                user_one=chat_room_obj.user_one,
                user_two=chat_room_obj.user_two,
            )
            Session.add(chat_room_db)
        else:
            chat_room_db.user_two = chat_room_obj.user_two
        Session.commit()
        return ChatRoomModel.from_orm(chat_room_db)

    def get_chat_room_by_id(self, chat_room_id: str) -> ChatRoomModel:
        """Get Chat Room By Id"""
        chat_room_db = (
            Session.query(ChatRoom).filter_by(chat_room_id=chat_room_id).first()
        )
        return ChatRoomModel.from_orm(chat_room_db)

    def fetch_user_by_id(self, user_id: str) -> UserModel:
        """Get User by id

        Fetch user object by querying on name
        :param name:
        :return:
        """
        user_db_obj = Session.query(User).filter_by(user_id=user_id).first()
        return UserModel.from_orm(user_db_obj)

    def save_messaage(self, chatroom_obj: ChatRoomModel, message_obj: MessageModel):
        """
        Saves a message to chatroom

        :param chatroom_obj:
        :param message_obj:
        :return:
        """
        message_obj = Message(
            chat_room_id=chatroom_obj.chat_room_id,
            user_id=message_obj.user_id,
            body=message_obj.body,
        )
        Session.add(message_obj)
        Session.commit()
        return MessageModel.from_orm(message_obj)

    def get_chat_room_messages(
        self, chatroom_obj: ChatRoomModel, page: int = 1, size: int = 20
    ) -> MessageModel:
        """
            Fetch all messages in a chat room

        :param chat_room_id:
        :param page:
        :param size:
        :return:
        """
        page = page - 1
        offset = page * size
        messages = (
            Session.query(Message)
            .filter_by(chat_room_id=chatroom_obj.chat_room_id)
            .order_by(Message.created_at.desc())
            .limit(size)
            .offset(offset)
            .all()
        )
        return [MessageModel.from_orm(i) for i in messages]
