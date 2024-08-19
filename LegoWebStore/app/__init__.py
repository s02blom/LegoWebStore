"""https://flask.palletsprojects.com/en/3.0.x/tutorial/"""

import os
from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "dev",
        DATABASE = os.path.join(app.instance_path, "LegoWebStore.sql"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_pyfile(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #Initilizes the database
    from . import db
    db.init_app(app)

    from . import frontpage
    app.register_blueprint(frontpage.blueprint)
    app.add_url_rule('/', endpoint='index')

    from . import admin
    app.register_blueprint(admin.blueprint)

    print("Flask instance created!")
    return app
