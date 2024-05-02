from flask import (Blueprint, flash, g, render_template, request, url_for)
#from db import get_connection

blueprint = Blueprint('frontpage', __name__)


@blueprint.route('/')
def index():
    print("Found / and index")
    return render_template("frontpage.html")