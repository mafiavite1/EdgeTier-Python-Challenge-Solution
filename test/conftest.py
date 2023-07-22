from typing import Generator

from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from app import app, database


@fixture(scope='function')
def test_database() -> Generator[SQLAlchemy, None, None]:
    """
    Set up the database.
    """
    database.drop_all()
    database.create_all()
    yield database
    database.drop_all()


@fixture(scope='function')
def client(test_database: SQLAlchemy) -> Generator[FlaskClient, None, None]:
    """
    Create a Flask test client.
    """
    app.testing = True
    yield app.test_client()
