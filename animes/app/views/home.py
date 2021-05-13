import re
from flask import Blueprint, jsonify, request
from flask.helpers import make_response
from app.models.anime import Anime
from app import db
import json

home = Blueprint('home', __name__)


@home.route('/', methods=['GET'])
def index():
    return jsonify({'mensaje': 'Bienvenido a mi api'})


@home.route('/anime', methods=['GET'])
def anime_all():
    ''' Metodo GET '''
    nombre = request.args.get('nombre', default=None, type=None)
    datos = []
    if nombre is None:
        datos = Anime().anime_query_all()
        respuesta = make_response(datos, 200)
        respuesta.headers['Content-Type'] = 'application/json'
        return respuesta
    else:
        nombre = nombre.lower()
        datos = Anime().anime_search(nombre)
        respuesta = make_response(datos, 200)
        respuesta.headers['Content-Type'] = 'application/json'
        return respuesta


@home.route('/anime/<anime>', methods=['GET'])
def anime_id(anime):
    '''Metodo GET uno'''
    anime = anime.lower()
    try:
        datos = Anime().anime_one(anime)
        respuesta = make_response(datos, 200)
        respuesta.headers['Content-Type'] = 'application/json'
        return respuesta
    except (AttributeError, TypeError):
        return jsonify({'mensaje': 'No existe'}), 404


@home.route('/anime/<id>', methods=['DELETE'])
def anime_delete(id: int):
    '''Metodo DELETE'''
    try:
        id = int(id)
        anime_delete = Anime().anime_one(id)
        print(anime_delete)
        if anime_delete:
            db.session.delete(anime_delete)
            db.session.commit()
            return jsonify({'mensaje': 'Eliminado'}), 200
        else:
            return jsonify({'mensaje': 'No existe id'}), 404
    except (AttributeError, ValueError):
        return jsonify({'mensaje': f'Error'}), 404



@home.route('/anime', methods=['POST'])
def anime_post():
    '''Metodo Post '''
    data = request.get_json()
    nombre = data['anime'].lower()
    anime = Anime().anime_one(nombre)
    if anime or nombre == '':
        return jsonify({'mensaje': f'Existe: {nombre}'})
    else:
        insertar = Anime(nombre, data['temporada'],
        data['fecha_publicacion'], data['fecha_termino'], 
        data['capitulos'], data['estado'])
        respuesta = make_response(insertar.anime_post(), 200)
        respuesta.headers['Content-Type'] = 'application/json'
        return respuesta
