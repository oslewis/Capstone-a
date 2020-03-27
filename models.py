
# ---------------- imports ---------------- #
from sqlalchemy import (
            Column,
            String,
            Integer,
            create_engine,
            Table,
            ForeignKey
            )
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_moment import Moment
import json
from array import array
from auth import AuthError, requires_auth
from sqlalchemy import func
from sqlalchemy.orm import session
import os
import math

# --------------------------------------------- #
os.environ['DATABASE_URL'] = 'postgres://ntzjdrpyajzsfi:ec557966c4bede18b28366c617ff37f2386872f2c2f1bff8e784f027e6767f34@ec2-35-168-54-239.compute-1.amazonaws.com:5432/d41a13fbfkrufc'
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask app and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# ----------- db.Models ------------- #

class Debt(db.Model):
    __tablename__ = 'Debt'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, default='')
    category = db.Column(db.ARRAY(db.String))
    amount = db.Column(db.Integer, nullable=False, default=0)
    balancesheets = db.relationship('BalanceSheet', backref='Debt', lazy=True)
    accounts = db.relationship('Account', backref='Debt', lazy=True)


    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'amount': self.amount
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Cashflow(db.Model):
    __tablename__ = 'Cashflow'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, default='')
    category = db.Column(db.ARRAY(db.String))
    amount = db.Column(db.Integer, nullable=False, default=0)
    balancesheets = db.relationship('BalanceSheet', backref='Cashflow', lazy=True)
    accounts = db.relationship('Account', backref='Cashflow', lazy=True)


    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount


    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'amount': self.amount,
            'total cashflow': session.query(func.count(Cashflow.amount))
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class BalanceSheet(db.Model):
    __tablename__ = 'Balancesheet'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    debt_id = db.Column(db.Integer, db.ForeignKey('Debt.id', ondelete='CASCADE'), nullable=True)
    cashflow_id = db.Column(db.Integer, db.ForeignKey('Cashflow.id', ondelete='CASCADE'), nullable=True)
    accounts = db.relationship('Account', backref='Balancesheet', lazy=True)

    def __init__(self, name):
        self.name = name


    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "total debt": session.query(func.count(Debt.amount)),
            "total cashflow": session.query(func.count(Cashflow.amount)),
            "total Cash": session.query(function.count(Account.cash))
        }


    def time_left(x, y, z):
        z = (y - x) + z
        l = z/30.42
        return l

class Account(db.Model):
    __tablename__ = 'Account'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    cash = db.Column(db.Integer, nullable=False, default=0)
    debt_id = db.Column(db.Integer, db.ForeignKey('Debt.id'), nullable=True)
    cashflow_id = db.Column(db.Integer, db.ForeignKey('Cashflow.id'), nullable=True)
    balancesheet_id = db.Column(db.Integer, db.ForeignKey('Balancesheet.id'), nullable=True)
