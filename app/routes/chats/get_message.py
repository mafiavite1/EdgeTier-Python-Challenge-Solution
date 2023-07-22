from app import app
from flask import jsonify
from app.functions import convert_to_json
from app.models import Message


# I created this just for testing purposes

@app.route("/messages", methods=["GET"])
def get_message():
    res = convert_to_json(Message.query.all())

    return jsonify(res)
