#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

import random

import click

import faker

import flask

import flask_sqlalchemy
import flask_migrate

from sqlalchemy.inspection import inspect
from sqlalchemy.sql import func


app = flask.Flask(__name__)
###app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
###app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://user:pass@host:port/database"
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{ os.environ['POSTGRESQL_USER'] }:{ os.environ['POSTGRESQL_PASSWORD'] }@{ os.environ['POSTGRESQL_HOST'] }:{ os.environ['POSTGRESQL_PORT'] }/{ os.environ['POSTGRESQL_DATABASE'] }"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_db = flask_sqlalchemy.SQLAlchemy(app)

app_migrate = flask_migrate.Migrate(app, app_db)


##########
# Models
##########

class User(app_db.Model):
    id = app_db.Column(app_db.Integer, primary_key=True)
    address = app_db.Column(app_db.Text)
    balance = app_db.Column(app_db.Integer)
    created_at = app_db.Column(app_db.DateTime(timezone=True), server_default=func.now())
    email = app_db.Column(app_db.String(80), unique=False, nullable=False)
    name = app_db.Column(app_db.String(100), nullable=False)
    giver_in = app_db.relationship('Move', backref='from_user',
        lazy=True, foreign_keys='Move.from_user_id')
    receiver_in = app_db.relationship('Move', backref='to_user',
        lazy=True, foreign_keys='Move.to_user_id')

    def __repr__(self):
        return f'<User {self.name}>'

    def serialize(self):
        something = 0
        for i in range(100000):
            something += i
        return {
            "id": self.id,
            "address": self.address,
            "balance": self.balance,
            "created_at": self.created_at,
            "email": self.email,
            "name": self.name,
        }

class Move(app_db.Model):
    id = app_db.Column(app_db.Integer, primary_key=True)
    amount = app_db.Column(app_db.Integer)
    created_at = app_db.Column(app_db.DateTime(timezone=True), server_default=func.now())
    from_user_id = app_db.Column(app_db.Integer, app_db.ForeignKey('user.id'), nullable=True)
    to_user_id = app_db.Column(app_db.Integer, app_db.ForeignKey('user.id'), nullable=True)

    def __repr__(self):
        return f'<Move {self.amount}>'

    def serialize(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "created_at": self.created_at,
            "from_user_id": self.from_user_id,
            "to_user_id": self.to_user_id,
        }


##########
# Routes
##########

def _serialize(query):
    if 'page' in flask.request.args:
        page = int(flask.request.args['page'])
    else:
        page = 1

    data = query.paginate(page=page)

    return {
        "total": data.total,
        "page": data.page,
        "pages": data.pages,
        "per_page": data.per_page,
        "items": [d.serialize() for d in data.items],
    }

@app.route('/', methods=['GET'])
def index():
    """Show API docs."""
    return "Hello world"

@app.route('/api/moves', methods=['GET'])
def api_moves():
    """List moves."""
    return _serialize(Move.query)

@app.route('/api/moves/<int:mid>', methods=['GET'])
def api_moves_mid(mid):
    """Return info about move ID."""
    return Move.query.filter_by(id=mid).first_or_404().serialize()

@app.route('/api/users', methods=['GET'])
def api_users():
    """List users."""
    return _serialize(User.query)

@app.route('/api/users/<int:uid>', methods=['GET'])
def api_users_uid(uid):
    """Return info about user ID."""
    return User.query.filter_by(id=uid).first_or_404().serialize()

@app.route('/api/users/search', methods=['GET'])
def api_users_search():
    """Search users where field 'by' contains substring 'text'."""
    assert 'by' in flask.request.args
    assert 'text' in flask.request.args
    search_by = flask.request.args['by']
    search_text = flask.request.args['text']

    query = User.query

    if search_by == 'name':
        query = query.filter(User.name.ilike('%' + search_text + '%'))
    elif search_by == 'email':
        query = query.filter(User.email.ilike('%' + search_text + '%'))
    elif search_by == 'address':
        query = query.filter(User.address.ilike('%' + search_text + '%'))
    else:
        raise Exception(f"Unknown search by field '{flask.request.args['by']}'")

    return _serialize(query)


##########
# CLI
##########

@click.command('test-data')
def test_data_command():
    """Populate initial test data to the DB."""
    fake = faker.Faker('cs_CZ')

    # Using this specific user in the test
    u = User()
    u.name = "Pavla Novotna"
    u.address = "Brno"
    u.email = "pavla@seznam.cz"
    u.balance = 1000
    app_db.session.add(u)

    for i in range(1000):
        u = User()
        u.name = fake.name()
        u.address = fake.address()
        u.email = fake.email()
        u.balance = fake.random_int()
        app_db.session.add(u)
        if i % 1000 == 0:
            app_db.session.flush()
    app_db.session.commit()

    users = User.query.all()
    for i in range(10000):
        from_user = random.choice(users)
        to_user = random.choice([item for item in users if item != from_user])
        m = Move()
        m.from_user = from_user
        m.to_user = to_user
        m.amount = int(fake.random_int() / 100) + 1
        app_db.session.add(m)
        if i % 1000 == 0:
            app_db.session.flush()
    app_db.session.commit()

app.cli.add_command(test_data_command)
