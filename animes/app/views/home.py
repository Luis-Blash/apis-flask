from flask import Blueprint, jsonify, request
from app.models.anime import Anime
from app import db
import json

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    return jsonify({'mensaje':'Bienvenido a mi api'})

@home.route('/anime', methods=['GET'])
def anime_all():
    '''GET 
    anime
    temporada
    fecha_publicacion
    fecha_termino
    capitulos
    estado
    '''
    animes = Anime.query.all()
    datos = []
    for i in animes:
        json_datos = {
            "id": i.id,
            "anime":i.anime,
            "temporada":i.temporada,
            "fecha_publicacion":i.fecha_publicacion,
            "fecha_termino":i.fecha_publicacion,
            "capitulos":i.capitulos,
            "estado":i.estado
        }
        datos.append(json_datos)
    datos = json.dumps(datos)
    return datos

@home.route('/anime/<anime>', methods=['GET'])
def anime_id(anime:str):
    try:
        anime = anime.lower()
        query_anime = Anime.query.filter_by(anime=anime).first()
        json_datos = {
                "id": query_anime.id,
                "anime":query_anime.anime,
                "temporada":query_anime.temporada,
                "fecha_publicacion":query_anime.fecha_publicacion,
                "fecha_termino":query_anime.fecha_publicacion,
                "capitulos":query_anime.capitulos,
                "estado":query_anime.estado
        }
        return json.dumps(json_datos)
    except AttributeError:
        return jsonify({'mensaje':f'No es String: {anime}'}),400

@home.route('/anime/<id>', methods=['DELETE'])
def anime_delete(id:int):
    anime_delete = Anime.query.filter_by(id=id).first()
    if anime_delete:
        db.session.delete(anime_delete)
        db.session.commit()
        return jsonify({'mensaje':'Eliminado'}),200
    else:
        return jsonify({'mensaje':f'No existe'}),404

@home.route('/anime', methods=['POST'])
def anime_post():
    '''Post 
    anime:string
    temporada:int
    fecha_publicacion:string
    fecha_termino:string
    capitulos:int
    estado:booleado
    '''
    data = request.get_json()
    nombre = data['nombre'].lower()
    anime = Anime.query.filter_by(anime=nombre).first()
    if anime or nombre == '':
        return jsonify({'mensaje':f'Existe: {nombre}'})
    else:
        try:
            temporada = data['temporada']
            fecha_publicacion = data['fecha_publicacion']
            fecha_termino = data['fecha_termino']
            capitulos = data['capitulos']
            estado = data['estado']
            if type(temporada)==int and type(fecha_termino)==str and type(fecha_publicacion)==str and type(estado)==bool and type(estado)==bool:
                agregar = Anime(anime=nombre, temporada=temporada, fecha_publicacion=fecha_publicacion,
                fecha_termino=fecha_termino, capitulos=capitulos,estado=estado)
                db.session.add(agregar)
                db.session.commit()
            return jsonify({'mensaje': f'Se inserto: {nombre}'}),201
        except:
            return jsonify({'mensaje': 'Verifica los nombres de las key'}),400