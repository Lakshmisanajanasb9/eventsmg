from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # This line will create the event table if it doesn't exist already
    with app.app_context():
        db.create_all()

    from .views import views
    from .routes.auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth)

    return app
