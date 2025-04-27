from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import stripe,os
from dotenv import load_dotenv
from flask_mail import Mail
from flask_migrate import Migrate

def create_fixed_categories(category):
    categories = ['Concerts', 'Sports', 'Festivals', 'Theatre']
    
    for category_name in categories:
        # Check if the category already exists to avoid duplicates
        if not category.query.filter_by(name=category_name).first():
            new_category = category(name=category_name)
            db.session.add(new_category)
    
    db.session.commit()

def init_categories():
    categories = [
        Category(name='Concerts'),
        Category(name='Sports'),
        Category(name='Festivals'),
        Category(name='Theatre')
    ]
    
    for category in categories:
        existing = Category.query.filter_by(name=category.name).first()
        if not existing:
            db.session.add(category)
    
    db.session.commit()

db = SQLAlchemy() 
from website.models import Category
mail = Mail()  
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    load_dotenv()
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "supersecretkey"
    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)


    from .models import Customer,Category

    # This line will create the event table if it doesn't exist already
    with app.app_context():
        db.create_all()
        init_categories()


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
