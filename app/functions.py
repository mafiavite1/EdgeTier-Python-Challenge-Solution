import re
from sqlalchemy.orm import class_mapper


def convert_row_to_json(row):
    # get column names
    mapper = class_mapper(row.__class__)
    columns = [column.key for column in mapper.columns]

    # create row in json format
    json_row = {}
    for column in columns:
        json_row[column] = getattr(row, column)

    return json_row

def convert_to_json(query_output):
    # append all json rows to a list
    return [convert_row_to_json(row) for row in query_output]

def blank_text(match):
    return "*" * len(match.group())

def hide_card(text):
    return re.sub(r"\b(?:\d[ -]*?){13,16}\b", blank_text, text)