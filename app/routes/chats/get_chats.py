from app import app
from flask import jsonify
from app.functions import convert_to_json
from app.models import Chat


# I created this just for testing purposes

@app.route("/chats", methods=["GET"])
def get_chats():
    res = convert_to_json(Chat.query.all())

    return jsonify(res)