from flask import Blueprint, jsonify, request, make_response
from app.models.anime import Anime
from app import db

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def index():
    return jsonify({'mensaje':'Bienvenido a mi api'})

@home.route('/anime', methods=['GET'])
def anime_all():
    return jsonify({'anime':'anime'})

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