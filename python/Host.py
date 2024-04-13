"""This file currently functions only as an example file
to see how flask will work. Code taken from: 
https://flask.palletsprojects.com/en/3.0.x/quickstart/#a-minimal-application"""

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"