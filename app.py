from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

app = Flask(__name__)

#Get DB URI
uri = os.environ.get("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SECRET_KEY'] = 'mysecret'

db = SQLAlchemy(app)

admin = Admin(app)

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    author = db.Column(db.String(30))
    date_finished = db.Column(db.DateTime)

db.init_app(app)

admin.add_view(ModelView(Book, db.session))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/books')
def books():
    books = db.Query("SELECT * FROM books")
    for book in books:
        print(f'{book}')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)