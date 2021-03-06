import os
import typing as ty
from random import randint

from flask import Flask

from . import public


def create_app(test_config: ty.Mapping[str, object] = None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    adm_t, adm_p = randint(10000, 99999), randint(10000, 99999)
    print('ADMIN SETTINGS:', adm_t, adm_p)
    app.config.from_mapping(SECRET_KEY='dev', )

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

    app.register_blueprint(public.bp)

    app.jinja_env.filters['zip'] = zip

    return app


if __name__ == "__main__":

    application = create_app()

    @application.route("/")
    def hello():
        return "<h1 style='color:blue'>Hello There!</h1>"

    application.run(host='0.0.0.0')
