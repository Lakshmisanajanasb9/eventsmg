from flask import Flask

from flask_sqlalchemy import SQLAlchemy

def create_app():

    db = SQLAlchemy()

    from .views import views

    app = Flask(__name__)

    app.register_blueprint(views, url_prefix='/')

    return app