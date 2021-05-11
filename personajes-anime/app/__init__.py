from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'password'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    from app.views.home import home

    app.register_blueprint(home, url_prefix='/')

    return app