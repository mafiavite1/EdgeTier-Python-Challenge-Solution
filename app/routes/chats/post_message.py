from http import HTTPStatus
from typing import Tuple
from app.functions import hide_card
from app import app, database
from flask import request
from app.models import Chat, Message
from app.schemas import message_schema
from jsonschema import validate, ValidationError


@app.route("/chats/<int:chat_id>/messages", methods=["POST"])
def post_message(chat_id: int) -> Tuple[str, int]:
    """
    Store a message. A message should be rejected if:

        - The chat hasn"t started yet.
        - The chat is already finished.
        - The user on the message is not handling the chat.
        - The message is more than 500 characters.

    Credit cards should also be blanked out with asterisks before storage.

    :param chat_id: Store a message for a chat.
    """

    # read chats and messages
    chat = Chat.query.get(chat_id)
    
    # validate input json
    try:
        message = request.get_json()
        validate(message, message_schema)
    except ValidationError as e:
        return str(e), HTTPStatus.BAD_REQUEST

    # check if chat has started
    if not chat:
        return "The chat has not started yet", HTTPStatus.NOT_FOUND
    
    # check if chat has ended
    if chat.handle_end:
        return (
            "Can not store a message after the chat has ended",
            HTTPStatus.BAD_REQUEST
        )

    # check if the user on the message is not handling the chat
    if str(message["user_id"]) != str(chat.user_id):
        return (
            f"Agent {message['user_id']} is not handling chat {chat.chat_id}",
            HTTPStatus.BAD_REQUEST
        )

    # check if text is larger than 500 characters
    if len(message["text"]) > 500:
        return "Text to long to be stored", HTTPStatus.BAD_REQUEST

    # hide credit card
    message["text"] = hide_card(message["text"])

    # post
    database.session.add(Message(chat_id=chat_id, **message))
    database.session.commit()

    return "Message posted successfully", HTTPStatus.CREATED
