from database import mongo_uri, collection_name
from flask import Flask, request
from flask_pymongo import PyMongo, abort
from utils import json_encode, check_for_missing_params
from functools import wraps

from cache import Cache

app = Flask(__name__)

app.config['MONGO_URI'] = mongo_uri()
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_AS_ASCII'] = False

mongo = PyMongo(app)

collection = mongo.db[collection_name()]

cache = Cache(threshold=10)


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

    missing_params = check_for_missing_params(params, required_params)

    if len(missing_params):
        return (json_encode({'errors': missing_params}), 400)

    students = collection.aggregate([
        {'$unwind': '$cursos'},
        {
            '$match': {
                'cursos.modalidade': {'$eq': params.get('modalidade')},
                'cursos.data_inicio': {
                    '$gte': params.get('data_inicio'),
                    '$lte': params.get('data_fim')
                }
            }
        },
        {'$sort': {'cursos.data_inicio': -1}}
    ])

    return (json_encode(students), 200)


@app.route("/students/<int:student_ra>", methods=['GET'])
def get_student(student_ra):

    if not student_ra:
        return (json_encode({'message': 'Missing student id'}), 400)

    if cache.is_cached(student_ra):

        cached_student = cache.retrieve(student_ra)

        return (json_encode(cached_student), 200)

    student = collection.find_one({
        'ra': {'$eq': student_ra}
    })

    if not student:
        return (json_encode({'message': 'Student not found'}), 404)

    cache.save(student_ra, student)

    return (json_encode(student), 200)


@app.route("/students/<int:student_ra>", methods=['DELETE'])
def delete_student(student_ra):

    if not student_ra:
        abort(404)

    params = request.args

    required_params = [
        'campus'
    ]

    missing_params = check_for_missing_params(params, required_params)

    if len(missing_params):
        return (json_encode({'errors': missing_params}), 400)

    student = collection.delete_one({
        '$and': [
            {'ra': {'$eq': student_ra}},
            {'cursos.campus': {'$eq': params.get('campus')}}
        ]
    })

    deleted_count = student.deleted_count

    if (deleted_count <= 0):
        return (json_encode({'deleted_count': deleted_count}), 202)

    return (json_encode({'deleted_count': deleted_count}), 200)


@app.route("/students", methods=['POST'])
def post_student():

    data = request.json

    required_params = [
        'nome',
        'idade_ate_31_12_2016',
        'ra',
        'cursos'
    ]

    missing_params = check_for_missing_params(data, required_params)

    if len(missing_params):
        return (json_encode({'errors': missing_params}), 400)

    data['ra'] = int(data['ra'])
    data['idade_ate_31_12_2016'] = int(data['idade_ate_31_12_2016'])

    inserted_id = collection.insert_one(data).inserted_id

    cache.save(data['ra'], data)

    return (json_encode({'message': 'Resource created'}), 201)


@app.route("/students/total", methods=['GET'])
def get_total_students():

    params = request.args

    required_params = [
        'campus',
        'data_inicio',
        'data_fim'
    ]

    missing_params = check_for_missing_params(params, required_params)

    if len(missing_params):
        return (json_encode({'errors': missing_params}), 400)

    total_students = collection.aggregate([
        {
            '$match': {
                'cursos.campus': params.get('campus').upper(),
                'cursos.data_inicio': {
                    '$gte': params.get('data_inicio'),
                    '$lte': params.get('data_fim'),
                }
            }
        },
        {
            '$count': 'total'
        }
    ])

    return json_encode(total_students)


@app.route("/courses", methods=['GET'])
def get_courses():

    params = request.args

    required_params = [
        'campus'
    ]

    missing_params = check_for_missing_params(params, required_params)

    if len(missing_params):
        return (json_encode({'errors': missing_params}), 400)

    courses = collection.aggregate([
        {'$project': {'_id': 0, 'campus': 1, 'cursos': 1}},
        {"$unwind": "$cursos"},
        {"$match": {"cursos.campus": params.get('campus').upper()}},
        {"$group": {
            "_id": '$cursos.campus',
            "cursos": {
                "$addToSet": {
                    "nome": "$cursos.curso",
                    "modalidade": '$cursos.modalidade',
                    'nive_do_curso': '$cursos.nivel_do_curso'
                }
            }
        }},
    ])

    return (json_encode(courses), 200)


app.run()
