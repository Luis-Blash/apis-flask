from flask import Blueprint, jsonify, request

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    return jsonify({'mensaje':'Bienvenido a mi api'})

@home.route('/anime', methods=['GET'])
def anime_all():
    return jsonify({'anime':'anime'})

@home.route('/anime', methods=['POST'])
def anime_post():
    nombre = request.get_json()
    return jsonify({'anime': nombre['nombre']})