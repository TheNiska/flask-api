# -*- coding: utf-8 -*-
from application import app
from flask import Blueprint, request, jsonify
from application.controller import Api

main_bp = Blueprint('main_bp', __name__, url_prefix="/api")
HEADER = {'Content-Type': 'application/json; charset=utf-8'}


# -------- STUFF -------------------------------------------------------------
@main_bp.route('/stuff', methods=['GET'])
def get_stuff_applications():
    page = int(request.args.get('page', 1))
    rows_per_page = int(request.args.get('rows_per_page', 25))
    if rows_per_page <= 0:
        rows_per_page = None
    order = request.args.get('order', 'date')

    response, status_code = (Api.get_stuff_applications(page,
                             rows_per_page, order))

    return (jsonify(response), status_code, HEADER)


@main_bp.route('/stuff', methods=['POST'])
def post_stuff_application():
    json_data = request.get_json()

    if json_data is None:
        return jsonify({'error': 'Invalid JSON data'}), 400

    response, status_code = Api.post_stuff_application(json_data)
    return (jsonify(response), status_code, HEADER)
# ----------------------------------------------------------------------------


# --------STUFF WITH ID-------------------------------------------------------
@main_bp.route('/stuff/<string:app_id>', methods=['GET'])
def get_stuff_application_by_id(app_id):
    response, status_code = Api.get_stuff_application_by_id(app_id)
    return (jsonify(response), status_code, HEADER)


@main_bp.route('/stuff/<string:app_id>', methods=['PUT'])
def put_stuff_application_by_id(app_id):
    json_data = request.get_json()

    if json_data is None:
        return jsonify({'error': 'Invalid JSON data'}), 400

    response, status_code = (Api
                             .put_stuff_application_by_id(app_id, json_data))

    return (jsonify(response), status_code, HEADER)


@main_bp.route('/stuff/<string:app_id>', methods=['PATCH'])
def patch_stuff_application_by_id(app_id):
    response, status_code = Api.patch_stuff_application_by_id(app_id)
    return (jsonify(response), status_code, HEADER)


@main_bp.route('/stuff/<string:app_id>', methods=['DELETE'])
def delete_stuff_application_by_id(app_id):
    response, status_code = Api.delete_stuff_application_by_id(app_id)
    return (jsonify(response), status_code, HEADER)
# ----------------------------------------------------------------------------


# ---------------- MONEY -----------------------------------------------------
@main_bp.route('/money', methods=['GET'])
def get_money():
    page = int(request.args.get('page', 1))
    rows_per_page = int(request.args.get('rows_per_page', 25))
    order = request.args.get('order', 'date')

    response, status_code = Api.get_money(page, rows_per_page, order)
    return (jsonify(response), status_code, HEADER)


@main_bp.route('/money', methods=['POST'])
def post_money():
    json_data = request.get_json()

    if json_data is None:
        return jsonify({'error': 'Invalid JSON data'}), 400

    response, status_code = Api.post_money(json_data)
    return (jsonify(response), status_code, HEADER)
# ----------------------------------------------------------------------------


# ------------------ MONEY WITH ID---------------------------------------------
@main_bp.route('/money/<string:money_id>', methods=['GET'])
def get_money_by_id(money_id):
    response, status_code = Api.get_money_by_id(money_id)
    return (jsonify(response), status_code, HEADER)


@main_bp.route('/money/<string:money_id>', methods=['PUT'])
def put_money_by_id(money_id):
    json_data = request.get_json()

    if json_data is None:
        return jsonify({'error': 'Invalid JSON data'}), 400

    response, status_code = Api.put_money_by_id(money_id, json_data)
    return (jsonify(response), status_code, HEADER)


@main_bp.route('/money/<string:money_id>', methods=['PATCH'])
def patch_money_by_id(money_id):
    response, status_code = Api.patch_money_by_id(money_id)
    return (jsonify(response), status_code, HEADER)


@main_bp.route('/money/<string:money_id>', methods=['DELETE'])
def delete_money_by_id(money_id):
    response, status_code = Api.delete_money_by_id(money_id)
    return (jsonify(response), status_code, HEADER)
# ----------------------------------------------------------------------------
