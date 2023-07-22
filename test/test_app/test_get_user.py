from http import HTTPStatus

from flask.testing import FlaskClient

from app import database
from app.models import User


def test_get_user(client: FlaskClient):
    """
    Test GET user route.
    :param client: Flask test client.
    """

    # Insert a test user.
    user = User(name="Test User")
    database.session.add(user)
    database.session.commit()

    # Request the user.
    response = client.get(f"/users/{user.user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json["userId"] == user.user_id
    assert response.json["name"] == user.name


def test_get_user_404(client: FlaskClient):
    """
    Test GET user route for a non-existent user ID.
    :param client: Flask test client.
    """
    response = client.get("/users/99999")
    assert response.status_code == HTTPStatus.NOT_FOUND
