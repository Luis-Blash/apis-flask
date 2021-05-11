from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()
BASE = os.path.abspath(os.path.dirname(__file__))
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'password'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(BASE+'/database',DB_NAME)

    db.init_app(app)

    from app.views.home import home

    app.register_blueprint(home, url_prefix='/')

    from .models.anime import Anime

    create_database(app)

    return app

def create_database(app):
    if not os.path.exists(BASE+'/database/'+DB_NAME):
        db.create_all(app=app)
        print("Creado base de datos")