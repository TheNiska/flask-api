# -*- coding: utf-8 -*-
from applications import db
from abc import ABC, abstractmethod


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))

    @classmethod
    def get_fields_list(cls):
        return {'id', 'username'}


class StuffApplications(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True)
    date = db.Column(db.Date)
    is_accepted = db.Column(db.Boolean, default=False)
    total_sum = db.Column(db.Float)

    # Указываем autor_id как ForeignKey и ссылаемся на модель Users
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('Users')

    @classmethod
    def get_fields_list(cls):
        return {'id', 'date', 'is_accepted', 'total_sum', 'author_id'}


class StuffApplicationRows(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True)
    stuff_application_id = db.Column(db.String(36))
    position = db.Column(db.Integer)
    subject = db.Column(db.String(150))
    count = db.Column(db.Integer)
    price = db.Column(db.Float)

    @classmethod
    def get_fields_list(cls):
        return {'id', 'stuff_application_id', 'position',
                'subject', 'count', 'price'}


class MoneyApplications(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True)
    date = db.Column(db.Date)
    is_accepted = db.Column(db.Boolean, default=False)
    is_issued = db.Column(db.Boolean, default=False)
    is_report_not_need = db.Column(db.Boolean, default=False)
    subject = db.Column(db.String(150))
    amount = db.Column(db.Float)
    report_file_name = db.Column(db.Text(64), unique=True, default=None)

    # Указываем autor_id как ForeignKey и ссылаемся на модель Users
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('Users')

    @classmethod
    def get_fields_list(cls):
        return {'id', 'date', 'is_accepted', 'is_issued', 'is_report_not_need',
                'subject', 'amount', 'report_file_name', 'author_id'}


class DBFuncs:
    # Функция для работы с БД в целом
    @classmethod
    def create(cls):
        db.create_all()
