import os
import json

from flask import (
    Flask, session, Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True,
                static_folder=os.path.dirname(
                os.path.abspath(__file__)) + '/static')

    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Add more configurations
    app.config['APP_FOLDER'] = 'app'
    app.config['TEMPLATES_FOLDER'] = os.path.join(app.config['APP_FOLDER'],'templates')
    app.config['UPLOAD_PATH'] = os.path.join(app.config['TEMPLATES_FOLDER'], 'upload.html')

    app.config['CACHING'] = False
    app.config['CACHING_MAX_DURATION'] = 60 * 60 * 2

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import endpoint_manager
    app.register_blueprint(endpoint_manager.bp)
    app.add_url_rule('/', endpoint='index')

    return app

app = create_app()