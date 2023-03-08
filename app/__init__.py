from flask import Flask
from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate(db)
admin = Admin()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Secret_key_development'

    app.config["SQLALCHEMY_DATABASE_URI"] = \
        "postgresql://postgres:postgres@172.17.0.2/recicla"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bootstrap.init_app(app)

    login_manager.init_app(app)

    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin.init_app(app)

    from app import routes
    routes.init_app(app)
    migrate.init_app(app)
    return app
