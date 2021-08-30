from flask.helpers import url_for
from flask_login.utils import login_required
from flask_wtf import form
from flask import render_template, flash, redirect, request
from portfolio import app, db
from portfolio.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user
from portfolio.models import User, Book, Project

""" ROUTES / APP """
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


""" ROUTES / AUTH """
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.username != 'ricardosaca':
            flash('You are not allowed to create a user')
            return redirect(url_for('home'))
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are a now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))