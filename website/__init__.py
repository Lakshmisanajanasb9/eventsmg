from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import stripe,os
from dotenv import load_dotenv

db = SQLAlchemy() 

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "supersecretkey"
    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    db.init_app(app)

    # This line will create the event table if it doesn't exist already
    with app.app_context():
        db.create_all()

    from .models import Customer

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))

    from .views import views
    from .routes.auth import auth
    from .routes.events import events
    from .routes.admin import admin 

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(events, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    return app
