from flask import Blueprint, jsonify, send_file
import savesoundcloud.api as api
from io import StringIO, BytesIO


api_blueprint = Blueprint('api_blueprint', __name__,
                  template_folder='templates',
                  static_folder='static')


@api_blueprint.route('/')
def index():
    return jsonify('hello')

@api_blueprint.route('/<user>/likes')
def user_likes(user):
    likes = api.likes_to_csv(api.get_likes(user))

    mem = BytesIO()
    mem.write(likes.encode('utf-8'))
    mem.seek(0)

    return send_file(
        mem,
        attachment_filename='{}_likes.csv'.format(user),
        as_attachment=True,
        mimetype='text/csv'
    )

@api_blueprint.route('/test')
def test():
    likes = api.csv_test()

    mem = BytesIO()
    mem.write(likes.encode('utf-8'))
    mem.seek(0)

    return send_file(
        mem,
        as_attachment=True,
        attachment_filename='test.csv',
        mimetype='text/csv'
    )