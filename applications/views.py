from applications import app
from flask import Blueprint, request, url_for, current_app
import json
from applications.model import DBFuncs

main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/stuff', methods=['GET', 'POST'])
def stuff():
    DBFuncs.create()
    return 'Hello World'
