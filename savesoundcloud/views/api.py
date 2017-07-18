from flask import Blueprint, jsonify, send_file, abort, request
import savesoundcloud.api as api


api_blueprint = Blueprint('api_blueprint', __name__,
                  template_folder='templates',
                  static_folder='static')

@api_blueprint.route('/user/<user>/<endpoint>')
def get_endpoint(user, endpoint):
    if endpoint not in api.ENDPOINTS:
        abort(404)

    return jsonify(api.consume(user, endpoint))


@api_blueprint.route('/user/<user>/<endpoint>.csv')
def get_csv(user, endpoint):
    if endpoint not in api.ENDPOINTS:
        abort(404)

    filename, file = api.to_csv(user, endpoint)

    return send_file(
        file,
        attachment_filename=filename,
        as_attachment=True,
        mimetype='text/csv'
    )


@api_blueprint.route('/find_user')
def find_users():
    return jsonify(api.find_users(request.args.get('term')))
