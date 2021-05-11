from app import db

class Anime(db.Model):
    __tablename__ = 'anime'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(30))

    def __init__(self, nombre):
        self.nombre = nombre

