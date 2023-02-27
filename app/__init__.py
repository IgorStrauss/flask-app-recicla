from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()

# migrate = Migrate(app, db)


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Secret_key_development'

    app.config["SQLALCHEMY_DATABASE_URI"] = \
        "postgresql://postgres:postgres@172.17.0.2/recicla"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    bootstrap.init_app(app)

    login_manager.init_app(app)

    from app import routes
    routes.init_app(app)

    return app
