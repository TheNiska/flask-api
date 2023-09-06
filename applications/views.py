from applications import app
from flask import Blueprint, request, url_for, current_app, jsonify
import json
from applications.model import DBFuncs
import applications.controller as Controller

main_bp = Blueprint('main_bp', __name__, url_prefix="/applications")


@main_bp.route('/stuff', methods=['GET'])
def get_stuff_applications():

    page = int(request.args.get('page', 1))
    rows_per_page = int(request.args.get('rows_per_page', 25))
    order = request.args.get('order', 'date')

    result = Controller.get_stuff_applications(page, rows_per_page, order)
    # Controller.post_new_application(test_data)

    return result


@main_bp.route('/stuff', methods=['POST'])
def post_stuff_application():
    json_data = request.get_json()

    if json_data is None:
        return jsonify({'error': 'Invalid JSON data'}), 400

    response = Controller.create_application(json_data)
    return response


# ----------------------------------------------------------------------------
@main_bp.route('/stuff/<string:app_id>', methods=['GET'])
def get_stuff_application_by_id(app_id):
    response = Controller.get_stuff_application_by_id(app_id)
    return response


@main_bp.route('/stuff/<string:app_id>', methods=['PUT'])
def get_stuff_application_by_id(app_id):
    json_data = request.get_json()

    if json_data is None:
        return jsonify({'error': 'Invalid JSON data'}), 400

    response = Controller.put_stuff_application_by_id(app_id, json_data)
    if response == 0:
        return jsonify({'error': 'Editing is prohibited'}), 405

    return response


@main_bp.route('/stuff/<string:app_id>', methods=['PATCH'])
def patch_stuff_application_by_id(app_id):
    response = Controller.patch_stuff_application_by_id(app_id)
    return response


@main_bp.route('/stuff/<string:app_id>', methods=['DELETE'])
def delete_stuff_application_by_id(app_id):
    response = Controller.delete_stuff_application_by_id(app_id)

    if response == 1:
        return jsonify({'Success': True}), 200
    else:
        return jsonify({'error': 'Unknown error'}), 500
# ----------------------------------------------------------------------------


