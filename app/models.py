from datetime import datetime

from sqlalchemy.orm import relationship

from .app import database
from sqlalchemy import Column, ForeignKey, Integer, Text, TIMESTAMP


class User(database.Model):
    user_id = Column(Integer, primary_key=True)

    # User's name. First and last name combined for simplicity.
    name = Column(Text, nullable=False, unique=True)


class Chat(database.Model):
    chat_id = Column(Integer, primary_key=True)

    # Time when the customer entered the queue to wait for an agent.
    created = Column(TIMESTAMP, default=datetime.utcnow(), nullable=False)

    # User that handled or is handling the chat (can be NULL if not yet handled).
    user_id = Column(Integer, ForeignKey(User.user_id))

    # Times when an agent started and finished handling a chat (can both be NULL).
    handle_start = Column(TIMESTAMP)
    handle_end = Column(TIMESTAMP)

    # List of messages in a chat.
    messages = relationship("Message", back_populates="chat")


class Message(database.Model):
    message_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey(Chat.chat_id))

    # Content of a message.
    text = Column(Text, nullable=False)

    # User that typed the message. Will be NULL for a customer.
    user_id = Column(Integer, ForeignKey(User.user_id))

    # Time the message was sent.
    sent_at = Column(TIMESTAMP, default=datetime.utcnow(), nullable=False)

    # Link to chat to which this message belongs.
    chat = relationship(Chat, back_populates="messages")

    # Link to the agent that typed the messages.
    user = relationship(User)
