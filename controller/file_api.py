from flask import make_response
from flask import jsonify, Blueprint, abort
import service_ops.tasks as tasks


file_bp = Blueprint('talent', __name__, url_prefix='/file')


@file_bp.before_request
def before_request():
    pass


@file_bp.route('/create/<file_name>', methods=['GET'])
def create_random_file(file_name):
    try:
        tasks.create_random_file_task.delay(file_name)
    except Exception as err:
        abort(make_response(jsonify(message=err.__str__(), params=file_name), 503,
                            {'Content-Type': 'application/json'}))

    response = make_response(jsonify(status=True, message='Creating a new file'), 200,
                             {'Content-Type': 'application/json'})
    return response


@file_bp.errorhandler(404)
def not_found(error):
    return 'Index Talent API - A Resource Not Found - ' + str(error), 404


@file_bp.errorhandler(500)
def internal_error(error):
    return 'Index Talent API - Internal Server Error - ' + str(error), 500
