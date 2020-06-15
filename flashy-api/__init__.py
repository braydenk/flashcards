import os

from flask import Flask


# application factory function
def create_app(test_config=None):
    # create and config the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flashy.sqlite')
    )

    if test_config is None:
        # load instance config
        app.config.from_pyfile('config.py', silent=True)
    else:
        # laod test config
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/ping')
    def pong():
        return 'pong'

    return app