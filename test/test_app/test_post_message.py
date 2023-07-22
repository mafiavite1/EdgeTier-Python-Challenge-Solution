from http import HTTPStatus
from flask.testing import FlaskClient
import pytest
from app import database
from app.models import Chat
from app.functions import hide_card
from datetime import datetime, timedelta


def test_post_messages_successful(client: FlaskClient):
    # create chat
    chat = Chat(chat_id="2", user_id="1", handle_start=datetime.utcnow())
    database.session.add(chat)
    database.session.commit()

    # post message
    response = client.post(f"/chats/2/messages", json={
        "text":"test message",
        "user_id": "1"
    })

    assert response.status_code == HTTPStatus.CREATED
    assert response.data.decode("utf-8") == "Message posted successfully"


def test_chat_not_started(client: FlaskClient):
    # create chat
    chat = Chat(chat_id="9999", user_id="1", handle_start=datetime.utcnow())
    database.session.add(chat)
    database.session.commit()

    # post message
    response = client.post(f"/chats/2/messages", json={
        "text":"test message",
        "user_id": "1"
    })

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.data.decode("utf-8") == "The chat has not started yet"


def test_chat_has_ended(client: FlaskClient):
    # create chat
    chat = Chat(
        chat_id="2", user_id="1",
        handle_start=datetime.utcnow() - timedelta(minutes=5),
        handle_end=datetime.utcnow())
    database.session.add(chat)
    database.session.commit()

    # post message
    response = client.post(f"/chats/2/messages", json={
        "text":"test message",
        "user_id": "1"
    })

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert (
        response.data.decode("utf-8") == \
        "Can not store a message after the chat has ended"
    )


def test_agent_not_handling_chat(client: FlaskClient):
    # create chat
    chat = Chat(chat_id="2", user_id="1", handle_start=datetime.utcnow())
    database.session.add(chat)
    database.session.commit()

    # post message
    response = client.post(f"/chats/2/messages", json={
        "text":"test message",
        "user_id": "9999"
    })

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data.decode("utf-8") == "Agent 9999 is not handling chat 2"


def test_message_greater_than_500(client: FlaskClient):
    # create chat
    chat = Chat(chat_id="2", user_id="1", handle_start=datetime.utcnow())
    database.session.add(chat)
    database.session.commit()

    # post message
    response = client.post(f"/chats/2/messages", json={
        "text":"""jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejejeje
                  jejejejejejejejejejejejejejejejejejejejejejejejejejejejej""",
        "user_id": "1"
    })

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data.decode("utf-8") == "Text to long to be stored"


@pytest.mark.parametrize("text", [
    "here is my card: 0324-2346-2534-1346",
    "0324-2346-2534-1346",
    "0324 2346 2534 1346",
    "0324 2346 25341346",
    "0324/2346/2534/1346"
    "how are you, here you have 0324 2346 2534 1346 byee :)"
])
def test_blank_credit_card(client: FlaskClient, text):
    text = hide_card(text)

    assert (
        ("****************" in text) or
        ("*****************" in text) or
        ("******************" in text) or
        ("*******************" in text)
    )
