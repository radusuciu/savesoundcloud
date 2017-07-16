from flask import Flask, make_response, jsonify
from http import HTTPStatus
import config.config as config

app = Flask(__name__)
app.config.from_object(config.config)

# Register blueprints
from savesoundcloud.views import home, api_blueprint
app.register_blueprint(home)
app.register_blueprint(api_blueprint, url_prefix='/api')

@app.errorhandler(HTTPStatus.UNAUTHORIZED)
def unauthorized(error):
    return make_response(jsonify({'error': error.description}), error.code)
