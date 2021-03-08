class Comidas:
    
    def __init__(self,nombre,precio,tipo,informacion,ingredientes):
        self.nombre =  nombre
        self.precio =  precio
        self.tipo = tipo
        self.informacion = informacion
        self.ingredientes = ingredientes

    def datosInsertar(self):
        return {
            "nombre": self.nombre,
            "precio":  self.precio,
            "tipo": self.tipo,
            "descripcion":{
                "informacion": self.informacion,
                "ingredientes": self.ingredientes
            }
        }

    def __str__(self):
        return f"{self.nombre}"