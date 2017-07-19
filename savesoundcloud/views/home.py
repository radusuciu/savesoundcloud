from flask import Blueprint, send_file, render_template, request
from savesoundcloud import redis
import savesoundcloud.api as api


home = Blueprint('home', __name__,
                 template_folder='templates',
                 static_folder='static')


@home.route('/')
def index():
    bootstrap = None
    return render_template('index.html', bootstrap=bootstrap)

@home.route('/<user>.zip')
def export_all(user):
    try:
        crumb = request.args.get('crumb')

        redis.set(crumb, 'started', ex=3600)
        file = api.export_all(user)
        redis.set(crumb, 'finished')

        return send_file(
            file,
            attachment_filename='{}.zip'.format(user),
            as_attachment=True,
            mimetype='application/zip, application/octet-stream'
        )
    except api.UserNotFound as e:
        redis.set(crumb, 'error')
        return ('', 204)


@home.route('/status/<crumb>')
def status(crumb):
    status = redis.get(crumb)

    if status and status.decode('utf-8') in ('finished', 'error'):
        redis.delete(crumb)

    return status or 'none'
