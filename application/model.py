# -*- coding: utf-8 -*-
from application import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))


class StuffApplications(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True)
    date = db.Column(db.Date)
    is_accepted = db.Column(db.Boolean, default=False)
    total_sum = db.Column(db.Float, default=0)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('Users')

    def to_json(self):
        json = {
            'id': self.id,
            'date': self.date.strftime('%d.%m.%Y'),
            'is_accepted': self.is_accepted,
            'total_sum': self.total_sum,
            'author': {
                'id': self.author.id,
                'username': self.author.username
            }
        }
        return json


class StuffApplicationRows(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True)
    stuff_application_id = db.Column(db.String(36))
    position = db.Column(db.Integer)
    subject = db.Column(db.String(150))
    count = db.Column(db.Integer)
    price = db.Column(db.Float)

    def to_json(self):
        json = {
            'position': self.position,
            'subject': self.subject,
            'count': self.count,
            'price': self.price
        }
        return json


class MoneyApplications(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True)
    date = db.Column(db.Date)
    is_accepted = db.Column(db.Boolean, default=False)
    is_issued = db.Column(db.Boolean, default=False)
    is_report_not_need = db.Column(db.Boolean, default=False)
    subject = db.Column(db.String(150))
    amount = db.Column(db.Float)
    report_file_name = db.Column(db.Text(64), unique=True, default=None)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('Users')

    def to_json(self, full=False):
        json = {
            'id': self.id,
            'date': self.date.strftime('%d.%m.%Y'),
            'is_accepted': self.is_accepted,
            'is_issued': self.is_issued,
            'amount': self.amount,
            'author': {
                'id': self.author.id,
                'username': self.author.username
            }
        }
        if full:
            json['is_report_not_need'] = self.is_report_not_need
            json['report_file_name'] = self.report_file_name

        return json


class DBFuncs:
    @classmethod
    def create(cls):
        db.create_all()

    @classmethod
    def delete_data(cls):
        try:
            db.session.query(StuffApplicationRows).delete()
            db.session.query(StuffApplications).delete()
            db.session.query(MoneyApplications).delete()
            db.session.commit()
        except Exception:
            db.session.rollback()
