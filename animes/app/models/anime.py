from app import db


class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime = db.Column(db.String(30), nullable=False)
    temporada = db.Column(db.Integer)
    fecha_publicacion = db.Column(db.String(15))
    fecha_termino = db.Column(db.String(15))
    capitulos = db.Column(db.Integer)
    estado = db.Column(db.Boolean)
