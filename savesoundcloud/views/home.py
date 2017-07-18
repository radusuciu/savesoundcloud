from flask import Blueprint, send_file, render_template, session, request
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

        session[crumb] = 'started'
        file = api.export_all(user)
        session[crumb] = 'finished'

        return send_file(
            file,
            attachment_filename='{}.zip'.format(user),
            as_attachment=True,
            mimetype='application/zip, application/octet-stream'
        )
    except api.UserNotFound as e:
        session[crumb] = 'error'
        return ('', 204)


@home.route('/status/<crumb>')
def status(crumb):
    status = session.get(crumb, 'none')

    if status in ('finished', 'error'):
        session.pop(crumb)

    return status
