from flask import (Blueprint, flash, g, render_template, request, url_for)
from . import db

blueprint = Blueprint('admin', __name__)

@blueprint.route("/admin", methods=("GET", "POST"))
def index():
    print("Found admins page")
    return render_template("admin.html")