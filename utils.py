from flask import jsonify
from bson.json_util import dumps

import json


def is_missing_required_params(args=[], required_params=[]):
    for param in required_params:
        if param not in args:
            return True
    return False


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
