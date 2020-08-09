from database import mongo_uri, collection_name
from flask import Flask, request, jsonify, make_response
from flask_pymongo import PyMongo, abort
from bson.json_util import dumps, loads, RELAXED_JSON_OPTIONS

from utils import json_encode, is_missing_required_params

import json

app = Flask(__name__)

app.config['MONGO_URI'] = mongo_uri()
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False

mongo = PyMongo(app)

collection = mongo.db[collection_name()]


@app.route("/", methods=['GET'])
def home():
    return "API is running"


@app.route("/students", methods=['GET'])
def get_students():

    params = request.args

    required_params = [
        'modalidade',
        'data_inicio',
        'data_final'
    ]

    if (is_missing_required_params(params, required_params)):
        abort(400)

    students = collection.find({
        '$and': [
            {'modalidade': {'$eq': params.get('modalidade')}},
            {'data_inicio': {
                '$gte': params.get('data_inicio'),
                '$lt': params.get('data_final')
            }}
        ]
    }).sort([('data_inicio', -1)])

    return (json_encode(students), 200)


@app.route("/courses", methods=['GET'])
def get_courses():

    params = request.args

    required_params = [
        'campus'
    ]

    if (is_missing_required_params(params, required_params)):
        abort(400)

    courses = collection.distinct('curso', {
        '$and': [
            {'campus': {'$eq': params.get('campus')}},
            {'curso': {'$ne': None}}
        ]
    })

    return (json_encode(courses), 200)


app.run()
