from http import HTTPStatus
from flask.testing import FlaskClient
import json
from configuration import insert_data


def test_insights(client: FlaskClient):
    insert_data()

    insights = client.get(f"/users/insights")
    chats = client.get(f"/chats")

    insights_output = json.loads(insights.data.decode("utf-8"))
    chats_output = json.loads(chats.data.decode("utf-8"))

    # count total amount of chats handeled
    chat_counts = [row["chatsHandled"] for row in insights_output]

    assert insights.status_code == HTTPStatus.OK

    # check that the total amount of chats handled does not exeed the existing chats
    assert len(chats_output) >= sum(chat_counts)