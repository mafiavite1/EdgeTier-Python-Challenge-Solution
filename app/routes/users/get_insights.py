from http import HTTPStatus
from app import app, database
from flask import jsonify
from app.models import Chat, User
from sqlalchemy import func


@app.route("/users/insights", methods=["GET"])
def get_insights():
    """
    Return the interactions completed and average handling time of every user.
    :return: JSON array:

    [
        {
            "userId": 1,
            "name": "Test User",
            "chatsHandled": 10,
            "averageHandlingSeconds": 120
        },
        ...
    ]

    """

    query = (
        database.session
        .query(
            Chat.user_id,
            User.name,
            func.count(Chat.user_id),
            func.avg(
                func.extract("epoch", Chat.handle_end) -
                func.extract("epoch", Chat.handle_start)
            )
        )
        .join(User, Chat.user_id == User.user_id, isouter=True)
        .group_by(Chat.user_id)
        .all()
    )

    result = []
    for user_id, name, count, time in query:
        result.append({
            "userId": user_id,
            "name": name,
            "chatsHandled": count,
            "averageHandlingSeconds": time
        })

    return jsonify(result), HTTPStatus.OK
