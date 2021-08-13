from flask import Flask, render_template, redirect, url_for, request
from flask_login.login_manager import LoginManager
from flask_login.utils import logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from forms import SigninForm, LoginForm
import os

from werkzeug.utils import redirect

""" Config Section """
app = Flask(__name__)
login = LoginManager(app)

#Config Database
uri = os.environ.get("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Initialize Flask-Admin and Flask-Login
login = LoginManager(app)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(20))
    # user_password = 


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    author = db.Column(db.String(30))
    date_finished = db.Column(db.Date)

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    pro_name = db.Column(db.String(50))
    pro_author = db.Column(db.String(30))
    pro_date = db.Column(db.Date)
    pro_desc = db.Column(db.String(100))
    pro_link = db.Column(db.Text)
    pro_embed = db.Column(db.Text)

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('index'))

#Initialize FLASK-Admin and Database
admin = Admin(app, index_view=MyAdminIndexView())
db.init_app(app)

#Set Views for FLASK-Admin
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Project, db.session))
admin.add_view(MyModelView(Book, db.session))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    books = Book.query.all()
    for book in books:
        print(book.name, book.author)
    return render_template('books.html', books=books)

@app.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/test', methods=['GET', 'POST'])
def test():
    form = SigninForm()

    if request.method == 'POST':
        return render_template('index.html')

    elif request.method == 'GET':
        return render_template('register.html', form=form)

@app.route('/login')
def login():
    user = User.query.get(1)
    login_user(user)
    return "Logged in"

@app.route('/logout')
def logout():
    logout_user()
    return "Logged out"

if __name__ == '__main__':
    app.run(debug=True)