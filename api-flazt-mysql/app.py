from flask import Flask, request, jsonify, make_response
# SQLAlchemy es una herramienta para los objetos relacionales SQL
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)

#------ SQLAlchemy
# creamos la url
# la base y su driver (si lo necesita)://usuario:contraseña@puerto/baseDatos
urldb= 'mysql+pymysql://root:@localhost/flaskrest'
# le decimos donde esta nuestra base
app.config['SQLALCHEMY_DATABASE_URI']=urldb
# con esto evitamos un Warning al conectar
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#Ahora le pasamos la base de datos
db = SQLAlchemy(app)
# ahora la instanciamos el Marshmallow
ma = Marshmallow(app)


# app de tareas ------

# ------- Tablas ---------
# una clase de tareas con el ORM
class Task(db.Model):
    # aqui declaramos la tabla que necesitamos
    # una columna que va ser llave primaria
    id = db.Column(db.Integer, primary_key=True)
    # un titulo que sera unico
    title = db.Column(db.String(70), unique= True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description
# con esto hacemos que crea todas nuestras tablas
db.create_all()


# creamos un esquema que nos permite interactuar con nuestra tabla
class TaskSchema(ma.Schema):
    class Meta:
        # le decimos campos que queremos interactuar en el esquema
        # son los que van a apareder 
        fields = ('id','title','description')

# con esto instanciamos para poder interactuar
# si queremos insertar, eliminar solo uno
task_schema =  TaskSchema()
# si queremos varios datos 
tasks_schema = TaskSchema(many=True)


@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json['title']
    description = request.json['description']
    # utilizando el metodo de task de su constructor le pasamos los datos
    new_task = Task(title, description)
    # guardamos en la base de datos
    db.session.add(new_task)
    # cargamos el servidor
    db.session.commit()
    #print(request.json) # con esto podemos ver lo que recibe con request.json
    return task_schema.jsonify(new_task)

# usando la misma direccion usamos get para recibir
@app.route('/tasks', methods=['GET'])
def get_tasks():
    # le decimos que desde la tabla queremos todo
    all_task =  Task.query.all()
    # utilizando el modelo
    result = tasks_schema.dump(all_task)
    #task_schema.jsonify(new_task) esto igual a solo jsonify
    return jsonify(result)

# si quiremos una tarea en especifico
@app.route('/tasks/<int:id>', methods=['GET'])
# utilizando el id que recibe
def get_task(id):
    # le decimos que solo queremos que obtenga la id
    task = Task.query.get(id)
    return task_schema.jsonify(task)

# si queremos actualizar una tarea
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    # primero obtenemos todas las tareas
    task =  Task.query.get(id)
    # vamos a pedir tambien un titulo y una descripcion
    # en forma de tipo json
    title = request.json['title']
    description = request.json['description']
    # esas variables las vamos a guardar en lo que acabamos de obtener
    task.title = title
    task.description =  description
    # guardamos cambios en la base de datos
    db.session.commit()
    return task_schema.jsonify(task)


# eliminar
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task =  Task.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message":"Bienvenido a mi api"})

if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")