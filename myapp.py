#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

import random

import click

import faker

import flask

import flask_sqlalchemy

from sqlalchemy.inspection import inspect
from sqlalchemy.sql import func



app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app_db = flask_sqlalchemy.SQLAlchemy(app)


##########
# Models
##########

class User(app_db.Model):
    id = app_db.Column(app_db.Integer, primary_key=True)
    address = app_db.Column(app_db.Text)
    balance = app_db.Column(app_db.Integer)
    created_at = app_db.Column(app_db.DateTime(timezone=True), server_default=func.now())
    email = app_db.Column(app_db.String(80), unique=True, nullable=False)
    name = app_db.Column(app_db.String(100), nullable=False)
    giver_in = app_db.relationship('Move', backref='from_user',
        lazy=True, foreign_keys='Move.from_user_id')
    receiver_in = app_db.relationship('Move', backref='to_user',
        lazy=True, foreign_keys='Move.to_user_id')

    def __repr__(self):
        return f'<User {self.name}>'

    def serialize(self):
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

@app.route('/', methods=['GET'])
def index():
    """Show API docs."""
    return "Hello world"

@app.route('/api/moves', methods=['GET'])
def api_moves():
    """List moves."""
    moves = Move.query.all()
    return {"count": len(moves), "results": [m.serialize() for m in moves]}

@app.route('/api/users', methods=['GET'])
def api_users():
    """List users."""
    users = User.query.all()
    return {"count": len(users), "results": [u.serialize() for u in users]}



##########
# CLI
##########

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    app.logger.info(f"Dropping tables {','.join([i.name for i in app_db.metadata.sorted_tables])}")
    app_db.drop_all()
    app.logger.info(f"Creating tables {','.join([i.name for i in app_db.metadata.sorted_tables])}")
    app_db.create_all()
    click.echo('Initialized the database.')

app.cli.add_command(init_db_command)

@click.command('test-data')
def test_data_command():
    """Populate initial test data to the DB."""
    fake = faker.Faker('cs_CZ')

    for i in range(10):
        u = User()
        u.name = fake.name()
        u.address = fake.address()
        u.email = fake.email()
        u.balance = fake.random_int()
        app_db.session.add(u)
    app_db.session.commit()

    users = User.query.all()
    for i in range(10):
        from_user = random.choice(users)
        to_user = random.choice([item for item in users if item != from_user])
        m = Move()
        m.from_user = from_user
        m.to_user = to_user
        m.amount = int(fake.random_int() / 100) + 1
        app_db.session.add(m)
    app_db.session.commit()

app.cli.add_command(test_data_command)
