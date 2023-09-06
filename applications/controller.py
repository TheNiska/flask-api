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
