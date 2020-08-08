from database import mongo_uri
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = mongo_uri()

mongo = PyMongo(app)


@app.route("/", methods=['GET'])
def home():
    return "API is running"


app.run()
