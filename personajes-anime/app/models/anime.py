from app import db

class Anime(db.Model):
    __tablename__ = 'anime'
    
    id = db.Column(db.Integer, primary_key=True)
    anime = db.Column(db.String(30))
    temporada = db.Column(db.Integer)
    fecha_publicacion = db.Column(db.String(15))
    fecha_termino = db.Column(db.String(15))
    capitulos = db.Column(db.Integer)
    estado = db.Column(db.Boolean)


    def __init__(self, nombre,temporada, fecha_publicacion, fecha_termino, capitulos, estado):
        self.nombre = nombre
        self.temporada = temporada
        self.fecha_publicacion = fecha_publicacion
        self.fecha_termino = fecha_termino
        self.capitulos = capitulos
        self.estado = estado

