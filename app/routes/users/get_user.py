from sqlalchemy import text

from app import app, database, models
from flask import jsonify, Response

from app.models import User


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int) -> Response:
    """
    Find and return a user by their ID.
    :param user_id: Requested user identifier.
    :return:        JSON object of the requested user.
    """
    user = models.User.query.get_or_404(user_id)
    return jsonify({"userId": user.user_id, "name": user.name})


def _get_user_raw_sql(user_id: int) -> User:
    """
    Example of getting a user using raw SQL for people who prefer that.
    :param user_id: Requested user.
    :return:        User row.
    """
    query = text('SELECT user_id, name FROM user WHERE user_id = :user_id')
    result = database.session.execute(query, {'user_id': user_id})
    return result.fetchone()
