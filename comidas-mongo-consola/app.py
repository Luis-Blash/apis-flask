import pymongo
from comidas import Comidas

MONGO_HOST =  "mongo"
PORT= 27017

# conexion
cliente = pymongo.MongoClient(MONGO_HOST,PORT)

# conexion de base de datos
db = cliente.comidas

# menu 
def main():
    seguir = True
    while seguir:
        opc = ""
        opc = input("\na) insertar\nb) Consultar\nc)Actualizar\nd)Eliminar\n")
        if opc.lower() == "a":
            insertar()
        elif opc.lower() == "b":
            consultar()
        elif opc.lower() == "c":
            actualizar()
        elif opc.lower() == "d":
            eliminar()
        else:
            print("no existe")
            
        opc =  input("\n¿Seguir?(S / N)")
        if(opc.lower() == "n"):
            seguir=False

# insertar
def insertar():
    nombre = input("\n¿Nombre?: ")
    precio = float(input("¿Precio?: "))
    tipo = input("¿Tipo?: ")
    informacion = input("Informacion de la comida: ")

    num = int(input("¿Cuantos ingredientes?"))
    ingredientes = []
    for i in range(num):
        ingredientes.append(input(f"{i}: "))
    
    # Clase de comidas donde me returna un json
    datos = Comidas(nombre,precio,tipo,informacion,ingredientes)
    # inserta a mongo
    db.comida.insert(datos.datosInsertar())

# consultar
def consultar():
    consulta = db.comida.find()
    for c in consulta:
        print(f"\nNombre: {c['nombre']}\nPrecio: {c['precio']}\nTipo: {c['tipo']}")
        print(f"Informacion:{c['descripcion']['informacion']}")
        print(f"Informacion:{c['descripcion']['ingredientes']}")
        print(f"---------------------------------------------")

# actualizar
def actualizar():
    print("\nComidas: ")
    for c in db.comida.find():
        print(f"{c['nombre']}")
    cual = input("¿Cual cambiar?")
    que = input("¿tipo?")
    db.comida.update({"nombre":f"{cual}"},{"$set":{"tipo":f"{que}"}})

# eliminar
def eliminar():
    for c in db.comida.find():
        print(f"{c['nombre']}")
    
    eliminar  = input("¿Cual eliminar?")
    db.comida.remove({"nombre":f"{eliminar}"})


if __name__ == '__main__':
    main()
