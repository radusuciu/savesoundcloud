from flask import Blueprint, render_template

home = Blueprint('home', __name__,
                 template_folder='templates',
                 static_folder='static')


@home.route('/')
def index():
    bootstrap = None
    return render_template('index.html', bootstrap=bootstrap)
