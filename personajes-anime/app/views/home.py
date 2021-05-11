from flask.json import jsonify
from flask import Blueprint, jsonify

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    return jsonify({'mensaje':'Bienvenido a mi api'})