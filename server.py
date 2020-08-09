from database import mongo_uri, collection_name
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps, loads, RELAXED_JSON_OPTIONS

from utils import json_encode

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

    errors = []

    if 'modalidade' not in params:
        errors.append({'message': 'modalidade param is missing'})

    if 'data_inicio' not in params:
        errors.append({'message': 'data_inicio param is missing'})

    if 'data_final' not in params:
        errors.append({'message': 'data_final param is missing'})

    if len(errors):
        return json_encode({'errors': errors})

    students = collection.find({
        '$and': [
            {'modalidade': {'$eq': params.get('modalidade')}},
            {'data_inicio': {
                '$gte': params.get('data_inicio'),
                '$lt': params.get('data_final')
            }}
        ]
    })

    return json_encode(students)


@app.route("/courses", methods=['GET'])
def get_courses():

    params = request.args

    errors = []

    if 'campus' not in params:
        errors.append({'message': 'campus param is missing'})

    if len(errors):
        return json_encode({'errors': errors})

    courses = collection.distinct('curso', {
        '$and': [
            {'campus': {'$eq': params.get('campus')}},
            {'curso': {'$ne': None}}
        ]
    })

    return json_encode(courses)


app.run()
