from flask import Blueprint, render_template
from portfolio.models import Project, Book

main =  Blueprint('main', __name__, template_folder='templates')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/books')
def books():
    books = Book.query.all()
    for book in books:
        print(book.name, book.author)
    return render_template('books.html', books=books)

@main.route('/projects')
def projects():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

