from app import db
import json

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anime = db.Column(db.String(30), nullable=False)
    temporada = db.Column(db.Integer)
    fecha_publicacion = db.Column(db.String(15))
    fecha_termino = db.Column(db.String(15))
    capitulos = db.Column(db.Integer)
    estado = db.Column(db.Boolean)

    def __init__(self, anime=None, temporada=None, fecha_publicacion=None, fecha_termino=None, capitulos=None, estado=None):
        self.anime =  anime
        self.temporada =  temporada
        self.fecha_termino =  fecha_termino
        self.fecha_publicacion =  fecha_publicacion
        self.capitulos =  capitulos
        self.estado =  estado
        self.datos = []
        self.animes = ''

    def anime_post(self):
        if type(self.estado) is bool and type(self.temporada) is int and type(self.capitulos) is int:
            agregar = Anime(
                anime= self.anime,
                temporada= self.temporada,
                fecha_publicacion= self.fecha_publicacion,
                fecha_termino= self.fecha_termino,
                capitulos= self.capitulos,
                estado= self.estado
                )
            db.session.add(agregar)
            db.session.commit()
            return {'mensaje':f"Se inserto {self.anime}"}
        else:
            return {'mensaje':"Falta datos"}

    def anime_query_all(self):
        self.animes = Anime.query.all()
        self.__json_datos_list()
        return json.dumps(self.datos)

    def anime_search(self,nombre):
        self.animes = Anime.query.filter(Anime.anime.like(f'%{nombre}%')).all()
        self.__json_datos_list()
        return json.dumps(self.datos)

    def __json_datos_list(self):
        for i in self.animes:
            self.datos.append(
                {
                    "id": i.id,
                    "anime": i.anime,
                    "temporada": i.temporada,
                    "fecha_publicacion": i.fecha_publicacion,
                    "fecha_termino": i.fecha_publicacion,
                    "capitulos": i.capitulos,
                    "estado": i.estado
                }
            )


    def anime_one(self,anime):
        if type(anime) is str:
            try:
                self.animes = Anime.query.filter_by(anime=anime).first()
                return self.__json_datos_one()
            except AttributeError:
                return False
        else:
            self.animes = Anime.query.filter_by(id=anime).first()
            return self.animes


    def __json_datos_one(self):
        datos = {
            "id": self.animes.id,
            "anime": self.animes.anime,
            "temporada": self.animes.temporada,
            "fecha_publicacion": self.animes.fecha_publicacion,
            "fecha_termino": self.animes.fecha_publicacion,
            "capitulos": self.animes.capitulos,
            "estado": self.animes.estado
        } 
        return datos
