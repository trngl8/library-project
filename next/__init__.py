import os

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap5

from . import db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    Bootstrap5(app)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'next.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    @app.route('/')
    def index():
        name = 'Library "3 Books"'
        return render_template('enter.html', name=name)

    return app
