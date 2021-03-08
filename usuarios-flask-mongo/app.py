import json
from flask import Flask, jsonify, request, Response
# flask mongo pymongo
from flask_pymongo import PyMongo
# modulo de cifrado
from werkzeug.security import generate_password_hash, check_password_hash
# bson para poder verlo, como un json
from bson import json_util
# bson objectid para poder convertir id de mongo a id legible
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://mongo:27017/usarios"
mongo = PyMongo(app)


# bienvenido
@app.route("/", methods=['GET'])
def index():
    return jsonify({"mesaje":"Bienvenido a mi api!!"})

# POST usuario
@app.route('/usuario', methods=['POST'])
def crear_comida():
    nombre =  request.json['nombre']
    contrasena =  request.json['contraseña']
    correo = request.json['correo']

    if nombre and contrasena and correo:
        hashed_contrasena = generate_password_hash(contrasena)
        #conectar con mongo
        id = mongo.db.usuario.insert_one(
            {"nombre": nombre,"contraseña": contrasena,"coreo": hashed_contrasena})

        respuesta = jsonify({
            "id": str(id),
            "nombre": nombre,
            "contraseña": correo,
            "coreo":correo
        })
        respuesta.status_code = 201
        return respuesta
    else:
        return {"mensaje":"user POST"}

# GET usuario
@app.route("/usuario", methods=['GET'])
def get_usuarios():
    # recibe los datos en formato de mongo bson
    usuarios = mongo.db.usuario.find()
    # convierto bson en json
    respuesta = json_util.dumps(usuarios)
    # y la cabecera que indica que es un json
    return Response(respuesta, mimetype='application/json')

#GET buscar solo uno
@app.route("/usuario/<id>", methods=['GET'])
def get_usuario(id):
    usuario = mongo.db.usuario.find_one({"_id":ObjectId(id)})
    respuesta = json_util.dumps(usuario)
    return Response(respuesta, mimetype='application/json')

# DELETE usuario
@app.route("/usuario/<id>", methods=['DELETE'])
def delete_usuario(id):
    mongo.db.usuario.delete_one({"_id":ObjectId(id)})
    respuesta = jsonify({"mensaje": "usuario "+ id + " eliminado "})
    return respuesta

# PUT actualizar
@app.route("/usuario/<id>", methods=['PUT'])
def update_usuario(id):
    nombre =  request.json['nombre']
    contrasena =  request.json['contraseña']
    correo = request.json['correo']

    if nombre and contrasena and correo:
        hashed_contrasena = generate_password_hash(contrasena)
        mongo.db.usuario.update_one({'_id': ObjectId(id)},{'$set':{
            "nombre": nombre,
            "contraseña": hashed_contrasena,
            "coreo": correo
        }})
        respuesta = jsonify({"mensaje":"usuario actualizado"})
        return respuesta


# http 404
@app.errorhandler(404)
def not_found(error=None):
    respuesta =  jsonify({
        "mensaje":'No encontrada ' + request.url,
        "estado":404
    })
    respuesta.status_code = 404
    return respuesta

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")