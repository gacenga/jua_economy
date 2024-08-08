from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

db = SQLAlchemy()
csrf = CSRFProtect()
login = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'jimwilly12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///microblog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    csrf.init_app(app)
    login.init_app(app)
    login.login_view = 'login'
    migrate.init_app(app, db)

    @login.user_loader
    def load_user(user_id):
        # Import the User model from the module where it's defined
        from .models import User
        return User.query.get(int(user_id))

    with app.app_context():
        from . import models
        from .routes import init_routes
        init_routes(app)
        db.create_all()

    return app
