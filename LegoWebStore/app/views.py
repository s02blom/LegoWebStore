"""This contains all the endpoints for the website"""
from flask import *

app = Flask(__name__)

@app.route("/")
def home(name=None):
    return render_template("home.html", name=name)