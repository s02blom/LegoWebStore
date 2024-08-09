from flask import (Blueprint, flash, g, render_template, request, url_for)
from . import db

blueprint = Blueprint('admin', __name__)

@blueprint.route("/admin", methods=("GET", "POST"))
def index():
    print("Found admins page")
    # I need a data set that contains All the data about and order, with
    # a sublist of information about the lego sets themselves. Unfortunatly I
    # belive it has to be split into two different sql statements to get the right 
    # structure in Python. 
    return render_template("admin.html")