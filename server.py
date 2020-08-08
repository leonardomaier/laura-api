import database

from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = database.get_mongo_uri()

mongo = PyMongo(app)

@app.route("/")
def home_page():
    return "Hello World"


app.run()
