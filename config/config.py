"""Main configuration file for project."""

import yaml
import os
import pathlib


PROJECT_NAME = 'savesoundcloud'
PROJECT_HOME_PATH = pathlib.Path(os.path.realpath(__file__)).parents[1]


# debug is true by default
DEBUG = bool(os.getenv('DEBUG', True))
_secrets_path = PROJECT_HOME_PATH.joinpath('config', 'secrets.yml')
_override_path = PROJECT_HOME_PATH.joinpath('config', 'secrets.override.yml')

# get our secrets
with _secrets_path.open() as f:
    _SECRETS = yaml.load(f)

# provide a mechanism for overriding some secrets
if _override_path.is_file():
    with _override_path.open() as f:
        _SECRETS.update(yaml.load(f))

class _Config(object):
    """Holds flask configuration to be consumed by Flask's from_object method."""

    # Flask
    DEBUG = False
    SECRET_KEY = _SECRETS['flask']['SECRET_KEY']
    JSONIFY_PRETTYPRINT_REGULAR = False

    # External APIs
    SOUNDCLOUD_CLIENT_ID = _SECRETS['soundcloud']['CLIENT_ID']
    SOUNDCLOUD_CLIENT_SECRET = _SECRETS['soundcloud']['CLIENT_SECRET']

class _DevelopmentConfig(_Config):
    """Configuration for development environment."""

    DEBUG = True

config = _DevelopmentConfig if DEBUG else _Config
