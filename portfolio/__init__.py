from flask import Flask, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView


db = SQLAlchemy()
login = LoginManager()
admin = Admin()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init db
    db.init_app(app)

    # init login manager
    login.init_app(app)
    login.login_view = 'login'

    from portfolio.models import Book, Project, User

    @login.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # init admin
    class MyModelView(ModelView):
        def is_accessible(self):
            return current_user.is_authenticated

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('main.index'))

    class MyAdminIndexView(AdminIndexView):
        def is_accessible(self):
            return current_user.is_authenticated

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('main.index'))


    #Initialize FLASK-Admin and Database
    admin.init_app(app, index_view=MyAdminIndexView())

    #Set Views for FLASK-Admin
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Project, db.session))
    admin.add_view(MyModelView(Book, db.session))

    # register blueprints
    from portfolio.main import main
    app.register_blueprint(main)
    from portfolio.auth import auth
    app.register_blueprint(auth)

    return app

