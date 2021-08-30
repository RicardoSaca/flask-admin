import click
from flask.cli import with_appcontext

from portfolio import db
from models import User, Book, Project

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()