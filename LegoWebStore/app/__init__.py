"""https://flask.palletsprojects.com/en/3.0.x/tutorial/"""

import os
from flask import flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(#Definelty not right for what we have got
        SECRET_KEY = "dev",
        DATABASE = os.path.join(app.instance_path, "LegoWebStore.sql"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_pyfile(test_config)

    try:
        os.makedirs(app.instance_path)  #Many not be needed ether
    except OSError:
        pass

    print("Flask instance created!")
    return app
