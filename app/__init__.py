import os
import json
import limits.storage

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask import (
    Flask, session, Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app(test_config=None):
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder=os.path.dirname(os.path.abspath(__file__)) + '/static')

    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'damp.sqlite'),
        )

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
    Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200/day", "50/hour"],  # this is default limit set for app
        storage_uri="memory://",
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
    app.config['TEMPLATES_FOLDER'] = os.path.join(app.config['APP_FOLDER'], 'templates')
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
