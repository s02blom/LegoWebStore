from flask import (Blueprint, flash, g, render_template, request, url_for)
from . import db
#from db import get_connection

blueprint = Blueprint('frontpage', __name__)


@blueprint.route('/')
def index():
    print("Found / and index")
    connection = db.get_connection()
    unavilable_sets = []
    with connection.cursor() as cursor:
        """Get things from server"""
        cursor.execute("SELECT * from LegoSet")
        avilable_sets = cursor.fetchall()
    return render_template("frontpage.html", avilable_sets=avilable_sets, unavilable_sets=unavilable_sets)