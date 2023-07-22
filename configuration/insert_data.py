from app import database
from app.models import Chat, Message, User
from datetime import datetime, timedelta


def insert_data():
    """
    Insert sample data into the database.
    """

    now = datetime.utcnow()

    # Insert users (agents).
    database.session.bulk_save_objects([
        User(name="Test User 1"),
        User(name="Test User 2"),
        User(name="Test User 3"),
    ])

    # Chat ID 1.
    database.session.add(
        Chat(
            created=now - timedelta(minutes=10),
            handle_start=now - timedelta(minutes=5),
            handle_end=now,
            user_id=1,
            messages=[
                Message(text='Hello, I need to cancel my reservation.', sent_at=now - timedelta(minutes=5)),
                Message(text='I can do that.', sent_at=now - timedelta(minutes=4), user_id=1),
                Message(text='That has been cancelled.', sent_at=now - timedelta(minutes=3), user_id=1),
                Message(text='Sound, thanks.', sent_at=now - timedelta(minutes=1)),
            ]
        )
    )

    # Chat ID 2: Active (unfinished) chat.
    database.session.add(
        Chat(
            created=now - timedelta(minutes=5),
            handle_start=now - timedelta(minutes=3),
            handle_end=None,
            user_id=1,
            messages=[
                Message(text='Your website is giving me an error.', sent_at=now - timedelta(minutes=3)),
                Message(text='Sorry to hear that, what is the error?', sent_at=now - timedelta(minutes=1), user_id=1)
            ]
        )
    )

    # Chat ID 3: Finished chat.
    database.session.add(
        Chat(
            created=now - timedelta(minutes=5),
            handle_start=now - timedelta(minutes=3),
            handle_end=now,
            user_id=3,
            messages=[
                Message(text='What are your opening hours?.', sent_at=now - timedelta(minutes=3)),
                Message(text='Monday to Friday, 9am to 6pm.', sent_at=now - timedelta(minutes=1), user_id=3),
                Message(text='Thanks.', sent_at=now - timedelta(minutes=1))
            ]
        )
    )

    # Chat ID 4: Finished chat.
    database.session.add(
        Chat(
            created=now - timedelta(minutes=25),
            handle_start=now - timedelta(minutes=21),
            handle_end=now - timedelta(minutes=11),
            user_id=3,
            messages=[
                Message(text="I'd like to make a complaint.", sent_at=now - timedelta(minutes=21)),
                Message(text="Please fill out a complaint form.", sent_at=now - timedelta(minutes=19), user_id=3),
                Message(text="You can find it on our website.", sent_at=now - timedelta(minutes=12), user_id=3),
                Message(text="OK I'll do that.", sent_at=now - timedelta(minutes=4))
            ]
        )
    )

    # Chat ID 5 and 6 are queuing.
    database.session.add(Chat(created=now - timedelta(minutes=10)))
    database.session.add(Chat(created=now - timedelta(minutes=15)))

    database.session.commit()
