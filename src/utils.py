import secrets

from pydantic import ValidationError

from src.models import ChatRoomModel, MessageModel, UserModel


class RandomIdGenerator:
    """Secure random id generator"""

    def __init__(self):
        """Opens wordlists and store in memory"""
        with open("wordlists/nouns.txt") as nouns, open(
            "wordlists/adjectives.txt"
        ) as adjectives:
            self._nouns = [noun.strip() for noun in nouns]
            self._adjectives = [adj.strip() for adj in adjectives]

    def _generate_user_id(self):
        """Generates random user id"""
        return f"{secrets.choice(self._nouns)}-{secrets.choice(self._nouns)}"

    def __call__(self, user_id=False):
        """Generates a secure random identifier"""
        if user_id:
            return self._generate_user_id()
        return f"{secrets.choice(self._adjectives)}-{secrets.choice(self._nouns)}-{secrets.choice(self._nouns)}"


def create_and_get_user(user_id: str, username: str) -> UserModel:
    """Creates User object from returns it"""
    try:
        user = UserModel(user_id=user_id, name=username, id=1)
    except ValidationError as e:
        # todo: we can parse(e.json()) and return readable exception to the user
        print(e.json())
    else:
        return user


def create_and_get_message(chat_room_id: str, user_id: str, body: str) -> MessageModel:
    """Creates Message object and returns it"""
    try:
        message = MessageModel(
            chat_room_id=chat_room_id, body=body, user_id=user_id, id=1
        )
    except ValidationError as e:
        print(e.json())
    else:
        return message


def create_and_get_chatroom(user_id: str, chat_room_id: str) -> ChatRoomModel:
    """Creates Chatroom object and returns it"""
    try:
        chatroom = ChatRoomModel(user_one=user_id, chat_room_id=chat_room_id, id=1)
    except ValidationError as e:
        print(e.json())
    else:
        return chatroom
