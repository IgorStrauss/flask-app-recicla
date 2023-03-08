from flask_admin.contrib.sqla import ModelView

from app import admin, db

from .models import User


def init_app(app):
    admin.name = app.config.TITLE
    admin.template_mode = "bootstrap3"
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
