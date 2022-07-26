from src.models import MessageModel
from datetime import datetime


def test_translate_bug():
    translate_bug = TranslateBug()
    message = MessageModel(message_id="ab1", body="I am a bug", timestamp=datetime.now())

    translate_bug.translate_to(message, "french")

    expected_message_body = "Je suis un bug"

    assert message.body == expected_message_body