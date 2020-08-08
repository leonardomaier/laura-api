from flask import jsonify
from bson.json_util import dumps

import json


def json_encode(documents):

    if isinstance(documents, dict):

        bson_to_str = dumps(documents)

        str_to_obj = json.loads(bson_to_str)

        return jsonify(str_to_obj)

    response = []

    for document in documents:

        bson_to_str = dumps(document)

        str_to_json = json.loads(bson_to_str)

        response.append(str_to_json)

    return jsonify(response)
