message_schema = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "user_id": {"type": "string"}
    },
    "required": ["text", "user_id"]
}