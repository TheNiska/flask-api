# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "lkjKljkK!kj89"

basedir = os.path.abspath(os.path.dirname(__file__))

app.json.ensure_ascii = False  # разрешает показывать кириллицу
app.json.compact = False  # отображает json с отступами

app.config['SQLALCHEMY_DATABASE_URI'] = ("sqlite:///" + os.path.join(
                                                      basedir, "data.sqlite"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from applications.views import main_bp
app.register_blueprint(main_bp)
