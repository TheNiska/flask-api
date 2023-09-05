# -*- coding: utf-8 -*-
from applications import db
import uuid


class UUID4Type(db.TypeDecorator):
    '''SQLite не имеет встроенного типа UUID4, поэтому создаём этот тип
    самостоятельно, внутри самой БД это будет строка длиной 36'''
    impl = db.String(36)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)
        return None

    def process_result_value(self, value, dialect):
        if value is not None:
            return uuid.UUID(value)
        return None


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))


class StuffApplications(db.Model):
    id = db.Column(UUID4Type, primary_key=True,
                   default=uuid.uuid4, unique=True)
    date = db.Column(db.Date)
    is_accepted = db.Column(db.Boolean, default=False)
    total_sum = db.Column(db.Float)

    # Указываем autor_id как ForeignKey и ссылаемся на модель Users
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('Users')


class StuffApplicationRows(db.Model):
    id = db.Column(UUID4Type, primary_key=True,
                   default=uuid.uuid4, unique=True)
    stuff_application_id = db.Column(UUID4Type)
    position = db.Column(db.Integer)
    subject = db.Column(db.String(150))
    count = db.Column(db.Integer)
    price = db.Column(db.Float)


class MoneyApplications(db.Model):
    id = db.Column(UUID4Type, primary_key=True,
                   default=uuid.uuid4, unique=True)
    date = db.Column(db.Date)
    is_accepted = db.Column(db.Boolean, default=False)
    is_issued = db.Column(db.Boolean, default=False)
    is_report_not_need = db.Column(db.Boolean, default=False)
    subject = db.Column(db.String(150))
    amount = db.Column(db.Float)
    report_file_name = db.Column(db.Text(64), unique=True)

    # Указываем autor_id как ForeignKey и ссылаемся на модель Users
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('Users')


class DBFuncs:
    # Функция для работы с БД в целом
    @classmethod
    def create(cls):
        db.create_all()
