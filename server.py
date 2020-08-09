from database import mongo_uri, collection_name
from flask import Flask, request
from flask_pymongo import PyMongo, abort
from utils import json_encode, is_missing_required_params
from functools import wraps

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
        'data_fim'
    ]

    if (is_missing_required_params(params, required_params)):
        abort(400)

    students = collection.find({
        '$and': [
            {'modalidade': {'$eq': params.get('modalidade')}},
            {'data_inicio': {
                '$gte': params.get('data_inicio'),
                '$lte': params.get('data_fim')
            }}
        ]
    }).sort([('data_inicio', -1)])

    return (json_encode(students), 200)


@app.route("/students/<int:student_ra>", methods=['GET'])
def get_student(student_ra):

    if not student_ra:
        abort(404)

    student = collection.find_one({
        'ra': {'$eq': student_ra}
    })

    if not student:
        abort(404)

    return (json_encode(student), 200)


@app.route("/students/<int:student_ra>", methods=['DELETE'])
def delete_student(student_ra):

    if not student_ra:
        abort(404)

    params = request.args

    required_params = [
        'campus'
    ]

    if (is_missing_required_params(params, required_params)):
        abort(400)

    student = collection.delete_one({
        '$and': [
            {'ra': {'$eq': student_ra}},
            {'campus': {'$eq': params.get('campus')}}
        ]
    })

    deleted_count = student.deleted_count

    if (deleted_count <= 0):
        return (json_encode({}), 202)

    return (json_encode({'deleted_count': deleted_count}), 200)


@app.route("/students", methods=['POST'])
def post_student():

    data = request.json

    required_params = [
        'nome',
        'idade_ate_31_12_2016',
        'ra',
        'campus',
        'municipio',
        'curso',
        'modalidade',
        'nivel_do_curso',
        'data_inicio'
    ]

    if (is_missing_required_params(data, required_params)):
        abort(400)

    data['ra'] = int(data['ra'])
    data['idade_ate_31_12_2016'] = int(data['idade_ate_31_12_2016'])

    inserted_id = collection.insert_one(data).inserted_id

    return (json_encode({inserted_id}), 201)


@app.route("/students/total", methods=['GET'])
def get_total_students():

    params = request.args

    required_params = [
        'campus',
        'data_inicio',
        'data_fim'
    ]

    if (is_missing_required_params(params, required_params)):
        abort(400)

    total_students = collection.find({
        'campus': {
            '$eq': params.get('campus')
        },
        'data_inicio': {
            '$gte': params.get('data_inicio'),
            '$lte': params.get('data_fim')
        }
    }).count()

    return json_encode({'total': total_students})


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
