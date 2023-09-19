# -*- coding: utf-8 -*-
from application import db
from application.model import (Users,
                               StuffApplications,
                               StuffApplicationRows,
                               MoneyApplications,
                               DBFuncs)
import uuid
import datetime
from pytz import timezone
from pydantic.dataclasses import dataclass
from pydantic import ValidationError
from dataclasses import asdict
import random
from flask import abort

# ----------------------------------------------------------------------------
'''Pydantic dataclasses with validation and initialization of default values.
They are here because I don't know a way (if there any) to directly integrate
them into ORM-classes.'''


@dataclass(kw_only=True)
class Stuff:
    id: str = None
    date: datetime.date = None
    is_accepted: bool = False
    total_sum: float = 0
    author_id: int

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.date is None:
            self.date = datetime.datetime.now(timezone('Europe/Moscow'))


@dataclass(kw_only=True)
class StuffRow:
    id: str = None
    stuff_application_id: str
    position: int
    subject: str
    count: int
    price: float

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())


@dataclass(kw_only=True)
class MoneyDC:
    id: str = None
    date: datetime.date = None
    is_accepted: bool = False
    is_issued: bool = False
    is_report_not_need: bool = False
    subject: str
    amount: float
    report_file_name: str = None
    author_id: int

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.date is None:
            self.date = datetime.datetime.now(timezone('Europe/Moscow'))
# ----------------------------------------------------------------------------


class Api:
    tz = timezone('Europe/Moscow')

    # -- Static utility methods ----------------------------------------------
    @staticmethod
    def _get_random_user() -> int:
        users = Users.query.all()
        user_id = random.choice(users).id
        return user_id

    @staticmethod
    def _get_ordered_query(model, order):
        query = model.query
        order_attr = getattr(model, order, None)
        if order_attr is not None:
            query = query.order_by(order_attr)
        return query
    # ------------------------------------------------------------------------

    @classmethod
    def get_stuff_applications(cls, page: int, rows_per_page: int, order: str):
        query = cls._get_ordered_query(StuffApplications, order)
        pagination = query.paginate(page=page, per_page=rows_per_page)

        result = {
            'page': page,
            'rows_per_page': rows_per_page,
            'data': [item.to_json() for item in pagination.items]
        }

        return result, 200

    @classmethod
    def post_stuff_application(cls, json_data):
        usr_id = cls._get_random_user()
        rows = json_data["rows"]

        # creating and validating Stuff dataclass
        try:
            new_app = Stuff(author_id=usr_id)
        except ValidationError as err:
            abort(500, {'error': err.errors()})

        total_sum = 0
        for row in rows:
            # creating and validating StuffRow dataclass
            try:
                new_row = StuffRow(stuff_application_id=new_app.id, **row)
            except ValidationError as err:
                db.session.rollback()
                abort(500, {'error': err.errors()})

            new_row_db = StuffApplicationRows(**asdict(new_row))
            new_app.total_sum += row["price"] * row["count"]
            db.session.add(new_row_db)

        try:
            new_app_db = StuffApplications(**asdict(new_app))
            db.session.add(new_app_db)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)

        return cls.get_stuff_application_by_id(new_app.id)

    @classmethod
    def get_stuff_application_by_id(cls, app_id: str):
        stuff_app = StuffApplications.query.get(app_id)
        if not stuff_app:
            abort(404)

        stuff_rows = (StuffApplicationRows.query
                      .filter_by(stuff_application_id=stuff_app.id)
                      .order_by(StuffApplicationRows.position)
                      .all())

        result = stuff_app.to_json()
        result['rows'] = [row.to_json() for row in stuff_rows]

        return result, 200

    @classmethod
    def put_stuff_application_by_id(cls, app_id: str, json_data):
        stuff_app = StuffApplications.query.get(app_id)
        if not stuff_app:
            abort(404)
        if stuff_app.is_accepted:
            abort(405)

        stuff_rows = (StuffApplicationRows.query
                      .filter_by(stuff_application_id=stuff_app.id)
                      .order_by(StuffApplicationRows.position)
                      .all())

        for row in stuff_rows:
            db.session.delete(row)  # deleting rows without commit

        rows = json_data['rows']
        total_sum = 0
        for row in rows:
            try:
                new_row = StuffRow(stuff_application_id=stuff_app.id, **row)
            except ValidationError as err:
                db.session.rollback()
                abort(500, {'error': err.errors()})

            new_row_db = StuffApplicationRows(**asdict(new_row))
            total_sum += row["price"] * row["count"]
            db.session.add(new_row_db)

        stuff_app.total_sum = total_sum
        stuff_app.date = datetime.datetime.now(cls.tz)

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)

        return cls.get_stuff_application_by_id(stuff_app.id)

    @classmethod
    def patch_stuff_application_by_id(cls, app_id: str):
        stuff_app = StuffApplications.query.get(app_id)
        if not stuff_app:
            abort(404)

        try:
            stuff_app.is_accepted = True
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)

        return cls.get_stuff_application_by_id(stuff_app.id)

    @classmethod
    def delete_stuff_application_by_id(cls, app_id: str):
        stuff_app = StuffApplications.query.get(app_id)
        if not stuff_app:
            abort(404)

        stuff_rows = (StuffApplicationRows.query
                      .filter_by(stuff_application_id=stuff_app.id)
                      .all())

        for row in stuff_rows:
            db.session.delete(row)

        try:
            db.session.delete(stuff_app)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)

        return {'Success': True}, 200

    @classmethod
    def get_money(cls, page: int, rows_per_page: int, order: str):
        query = cls._get_ordered_query(MoneyApplications, order)
        pagination = query.paginate(page=page, per_page=rows_per_page)

        result = {
            'page': page,
            'rows_per_page': rows_per_page,
            'data': [item.to_json() for item in pagination.items]
        }

        return result, 200

    @classmethod
    def post_money(cls, json_data):
        usr_id = cls._get_random_user()

        try:
            money_dc = MoneyDC(author_id=usr_id, **json_data)
        except ValidationError as err:
            db.session.rollback()
            abort(500, {'error': err.errors()})

        money = MoneyApplications(**asdict(money_dc))

        try:
            db.session.add(money)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)

        return cls.get_money_by_id(money_dc.id)

    @classmethod
    def get_money_by_id(cls, money_id: str):
        money = MoneyApplications.query.get(money_id)
        if not money:
            abort(404)

        result = money.to_json(full=True)
        return result, 200

    @classmethod
    def put_money_by_id(cls, money_id: str, json_data):
        money = MoneyApplications.query.get(money_id)
        if not money:
            abort(404)

        if money.is_accepted:
            abort(405)

        try:
            money_dc = MoneyDC(**json_data)
        except ValidationError as err:
            db.session.rollback()
            abort(500, {'error': err.errors()})

        money.is_report_not_need = money_dc.is_report_not_need
        money.subject = money_dc.subject
        money.amount = money_dc.amount
        money.date = money_dc.date

        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)

        return cls.get_money_by_id(money.id)

    @classmethod
    def patch_money_by_id(cls, money_id: str):
        money = MoneyApplications.query.get(money_id)
        if not money:
            abort(404)

        money.is_accepted = True
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)

        return cls.get_money_by_id(money.id)

    @classmethod
    def delete_money_by_id(cls, money_id: str):
        money = MoneyApplications.query.get(money_id)
        if not money:
            abort(404)

        try:
            db.session.delete(money)
            db.session.commit()
        except Exception:
            db.session.rollback()
            abort(500)

        return {'Success': True}, 200

    @classmethod
    def add_user(cls, username: str) -> None:
        user = Users(username=username)
        db.session.add(user)
        db.session.commit()
