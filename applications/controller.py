# -*- coding: utf-8 -*-
from applications import db
from applications.model import (Users,
                                StuffApplications,
                                StuffApplicationRows,
                                MoneyApplications,
                                DBFuncs)
from flask import jsonify
import json
import uuid
from datetime import datetime
from pytz import timezone


def get_stuff_applications(page: int, rows_per_page: int, order: str):
    '''Функция возвращает json ответ'''

    query = StuffApplications.query

    if rows_per_page < 0:
        rows_per_page = None

    if order == 'is_accepted':
        query = query.order_by(StuffApplications.is_accepted)
    elif order == 'id':
        query == query.order_by(StuffApplications.id)
    elif order == 'total_sum':
        query == query.order_by(StuffApplications.total_sum)
    elif order == 'author_id':
        query == query.order_by(StuffApplications.author_id)
    elif order == 'date':
        query == query.order_by(StuffApplications.date)
    else:
        query == query.order_by(StuffApplications.date)

    # Вычисляем индексы элементов для пагинации
    if rows_per_page is not None:
        start_index = (page - 1) * rows_per_page
        end_index = start_index + rows_per_page
        query = query.slice(start_index, end_index)

    items = query.all()

    # Преобразуем результат в формат json
    result = {
        'page': page,
        'rows_per_page': rows_per_page,
        'data': [
            {
                'id': item.id,
                'date': item.date.strftime('%d.%m.%Y'),
                'is_accepted': item.is_accepted,
                'total_sum': item.total_sum,
                'author': {
                    'id': item.author.id,
                    'username': item.author.username
                }
            }
            for item in items
        ]
    }

    return jsonify(result)


def add_user(username: str) -> None:
    user = Users(username=username)
    db.session.add(user)
    db.session.commit()


def create_application(json_data):
    tz = timezone('Europe/Moscow')

    # -- ТРЕБУДЕТСЯ ОПРЕДЕЛЕНИЕ АВТОРСТВА ЧЕРЕЗ ВНЕШНИЙ МОДУЛЬ --
    author_id = 2
    # -- ТРЕБУДЕТСЯ ОПРЕДЕЛЕНИЕ АВТОРСТВА ЧЕРЕЗ ВНЕШНИЙ МОДУЛЬ --

    rows = json_data["rows"]
    total_sum = 0
    application_uuid = str(uuid.uuid4())  # создание uuid4 для заявки

    # Сначала записываем в базу данных StuffApplicationRows строки товаров --
    for row in rows:
        new_row = StuffApplicationRows()
        new_row.id = str(uuid.uuid4())
        new_row.stuff_application_id = application_uuid
        new_row.position = row["position"]
        new_row.subject = row["subject"]
        new_row.price = row["price"]
        new_row.count = row["count"]
        total_sum += row["price"]
        db.session.add(new_row)
    # -----------------------------------------------------------------------

    # Затем записываем в базу данных StuffApplications саму заявку ----------
    new_application = StuffApplications()
    new_application.id = application_uuid
    new_application.date = datetime.now(tz)
    new_application.total_sum = total_sum
    new_application.author_id = author_id
    db.session.add(new_application)
    # -----------------------------------------------------------------------
    db.session.commit()

    # Далее работа с ответом сервера
    stuff_app = StuffApplications.query.get(application_uuid)
    stuff_rows = (StuffApplicationRows.query
                  .filter_by(stuff_application_id=application_uuid)
                  .order_by(StuffApplicationRows.position)
                  .all())

    result = {
        'id': stuff_app.id,
        'date': stuff_app.date.strftime('%d.%m.%Y'),
        'is_accepted': stuff_app.is_accepted,
        'total_sum': stuff_app.total_sum,
        'author': {
            'id': stuff_app.author.id,
            'username': stuff_app.author.username
        },
        'rows': [
            {
                'position': item.position,
                'subject': item.subject,
                'count': item.count,
                'price': item.price

            }
            for item in stuff_rows
        ]
    }

    return jsonify(result)


def get_stuff_application_by_id(app_id: str):
    '''Обработать ошибку если не найдено'''
    stuff_app = StuffApplications.query.get(app_id)
    stuff_rows = (StuffApplicationRows.query
                  .filter_by(stuff_application_id=stuff_app.id)
                  .order_by(StuffApplicationRows.position)
                  .all())

    result = {
        'id': stuff_app.id,
        'date': stuff_app.date.strftime('%d.%m.%Y'),
        'is_accepted': stuff_app.is_accepted,
        'total_sum': stuff_app.total_sum,
        'author': {
            'id': stuff_app.author.id,
            'username': stuff_app.author.username
        },
        'rows': [
            {
                'position': item.position,
                'subject': item.subject,
                'count': item.count,
                'price': item.price

            }
            for item in stuff_rows
        ]
    }

    return jsonify(result)


def put_stuff_application_by_id(app_id: str, json_data):
    '''Удалять только строки, или заново и всю карточку новую создавать
    с новыми id и датой?'''
    stuff_app = StuffApplications.query.get(app_id)
    if stuff_app.is_accepted:
        return 0

    # Удаляем старые строки товаров -----------------------------------------
    stuff_rows = (StuffApplicationRows.query
                  .filter_by(stuff_application_id=stuff_app.id)
                  .order_by(StuffApplicationRows.position)
                  .all())
    for row in stuff_rows:
        db.session.delete(row)
    db.session.commit()
    # -----------------------------------------------------------------------

    rows = json_data['rows']
    total_sum = 0
    # Записываем в базу данных StuffApplicationRows новые строки ------------
    for row in rows:
        new_row = StuffApplicationRows()
        new_row.id = str(uuid.uuid4())
        new_row.stuff_application_id = stuff_app.id
        new_row.position = row["position"]
        new_row.subject = row["subject"]
        new_row.price = row["price"]
        new_row.count = row["count"]
        total_sum += row["price"]
        db.session.add(new_row)
    # -----------------------------------------------------------------------

    stuff_app.total_sum = total_sum
    db.session.commit()

    # используем уже написанную ранее функция для ответа
    result = get_stuff_application_by_id(stuff_app.id)
    return result


def patch_stuff_application_by_id(app_id: str):
    stuff_app = StuffApplications.query.get(app_id)
    stuff_app.is_accepted = True
    db.session.commit()
    result = get_stuff_application_by_id(stuff_app.id)
    return result


def delete_stuff_application_by_id(app_id: str):
    '''Удаляем карточу и связанные с ней строки'''
    stuff_app = StuffApplications.query.get(app_id)
    current_id = stuff_app.id
    db.session.delete(stuff_app)

    stuff_rows = (StuffApplicationRows.query
                  .filter_by(stuff_application_id=current_id)
                  .order_by(StuffApplicationRows.position)
                  .all())
    for row in stuff_rows:
        db.session.delete(row)
    db.session.commit()
    return 1


def get_money(page: int, rows_per_page: int, order: str):

    query = MoneyApplications.query

    if rows_per_page < 0:
        rows_per_page = None

    if order == 'is_accepted':
        query = query.order_by(MoneyApplications.is_accepted)
    elif order == 'id':
        query == query.order_by(MoneyApplications.id)
    elif order == 'is_issued':
        query == query.order_by(MoneyApplications.is_issued)
    elif order == 'is_report_not_need':
        query == query.order_by(MoneyApplications.is_report_not_need)
    elif order == 'date':
        query == query.order_by(MoneyApplications.date)
    elif order == 'subject':
        query == query.order_by(MoneyApplications.subject)
    elif order == 'amount':
        query == query.order_by(MoneyApplications.amount)
    elif order == 'report_file_name':
        query == query.order_by(MoneyApplications.report_file_name)
    elif order == 'author_id':
        query == query.order_by(MoneyApplications.author_id)
    else:
        query == query.order_by(MoneyApplications.date)

    # Вычисляем индексы элементов для пагинации
    if rows_per_page is not None:
        start_index = (page - 1) * rows_per_page
        end_index = start_index + rows_per_page
        query = query.slice(start_index, end_index)

    items = query.all()

    # Преобразуем результат в формат json
    result = {
        'page': page,
        'rows_per_page': rows_per_page,
        'data': [
            {
                'id': item.id,
                'date': item.date.strftime('%d.%m.%Y'),
                'is_accepted': item.is_accepted,
                'is_issued': item.is_issued,
                'amount': item.amount,
                'author': {
                    'id': item.author.id,
                    'username': item.author.username
                }
            }
            for item in items
        ]
    }

    return jsonify(result)


def post_money(json_data):
    tz = timezone('Europe/Moscow')

    # -- ТРЕБУДЕТСЯ ОПРЕДЕЛЕНИЕ АВТОРСТВА ЧЕРЕЗ ВНЕШНИЙ МОДУЛЬ --
    author_id = 2
    # -- ТРЕБУДЕТСЯ ОПРЕДЕЛЕНИЕ АВТОРСТВА ЧЕРЕЗ ВНЕШНИЙ МОДУЛЬ --

    new_uuid = str(uuid.uuid4())

    new_money = MoneyApplications()
    new_money.id = new_uuid
    new_money.date = datetime.now(tz)
    new_money.is_report_not_need = json_data['is_report_not_need']
    new_money.subject = json_data['subject']
    new_money.amount = json_data['amount']
    new_money.report_file_name = ""
    new_money.author_id = author_id

    db.session.add(new_money)
    db.session.commit()

    money = MoneyApplications.query.get(new_uuid)
    result = {
        'id': money.id,
        'date': money.date.strftime('%d.%m.%Y'),
        'is_accepted': money.is_accepted,
        'is_issued': money.is_issued,
        'is_report_not_need': money.is_report_not_need,
        'report_file_name': money.report_file_name,
        'amount': money.amount,
        'author': {
            'id': money.author.id,
            'username': money.author.username
        }
    }

    return jsonify(result)


def get_money_by_id(money_id: str):
    '''Обработать ошибку если не найдено'''
    money = MoneyApplications.query.get(money_id)

    result = {
        'id': money.id,
        'date': money.date.strftime('%d.%m.%Y'),
        'is_accepted': money.is_accepted,
        'is_issued': money.is_issued,
        'is_report_not_need': money.is_report_not_need,
        'report_file_name': money.report_file_name,
        'amount': money.amount,
        'author': {
            'id': money.author.id,
            'username': money.author.username
        }
    }

    return jsonify(result)


def put_money_by_id(money_id: str, json_data):
    '''Обновляется ли дата'''
    money = MoneyApplications.query.get(money_id)
    if money.is_accepted:
        return 0

    money.is_report_not_need = json_data['is_report_not_need']
    money.subject = json_data['subject']
    money.amount = json_data['amount']
    db.session.commit()

    result = get_money_by_id(money.id)
    return result


def patch_money_by_id(money_id: str):
    money = MoneyApplications.query.get(money_id)
    money.is_accepted = True
    db.session.commit()
    result = get_money_by_id(money.id)
    return result


def delete_money_by_id(money_id: str):
    money = MoneyApplications.query.get(money_id)
    db.session.delete(money)
    db.session.commit()
    return 1
