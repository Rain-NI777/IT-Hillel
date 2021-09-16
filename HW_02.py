import requests
import sys
import faker
import flask
import datetime
from flask import Flask
from faker import Faker
import random

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/now")
def get_current_time():
    return str(datetime.datetime.now())


@app.route("/pipfile")
def get_pipfile():
    my_file = open('Pipfile.lock', 'r', encoding='UTF-8')
    return my_file.read()


@app.route("/random_students")
def get_random_students():
    fake = Faker('UK')
    return str(f'Студент ' + fake.name())


app.run()

