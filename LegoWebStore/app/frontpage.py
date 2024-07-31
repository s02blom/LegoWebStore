from flask import (Blueprint, flash, g, render_template, request, url_for)
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, IntegerField
from wtforms.validators import DataRequired
from . import db

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

class NewOrder(FlaskForm):
    company_name = StringField("Company name", validators=[DataRequired()])
    company_country = StringField("International two letter code of your country", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    street_adress = StringField("Street adress", validators=[DataRequired()])
    post_code = StringField("Post code", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    shipping_country = StringField("International two letter code of your country", validators=[DataRequired()])

    lego_sets = FieldList(IntegerField("Lego set id", validators=[DataRequired()]), 
                          IntegerField("Quantity", validators=[DataRequired()]), 
                          min_entries=1, max_entries=100)


@blueprint.route('/order', methods=("POST",))
def order():
    
    pass