from flask import (Blueprint, flash, g, render_template, request, url_for)
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, IntegerField
from wtforms.validators import DataRequired

blueprint = Blueprint('admin', __name__)

@blueprint.route("/admin", methods=("GET", "POST"))
def index():
    print("Found admins page")
    connection = db.get_connection()
    new_lego_set = New_Lego_Set()
    if new_lego_set.validate_on_submit():
        lego_set_sql = """
        INSERT INTO LegoSet (Name, Price) VALUES
        (%(name)s, %(price)s)
        """
        new_lego_set_data = {
            "name": new_lego_set.name.data,
            "price": new_lego_set.price.data
        }
        lego_set_content_sql = """
        INSERT INTO LegoSetContent (LegoSet, LegoBrick, Quantity) VALUES
        (%(lego_set)s, %(lego_brick)s, %(quantity)s)
        """
        with connection.cursor() as cursor:
            cursor.execute(lego_set_sql, new_lego_set_data)
            cursor.fetchall()
            lego_set_id = cursor.lastrowid
            for i in range(len(new_lego_set.lego_bricks_id)):
                lego_set_content_data = {
                    "lego_set": lego_set_id,
                    "lego_brick": new_lego_set.lego_bricks_id[i].data,
                    "quantity": new_lego_set.lego_bricks_quantity[i].data
                }
                cursor.execute(lego_set_content_sql, lego_set_content_data)
                cursor.fetchall()
    return render_template("admin.html", lego_set_form=new_lego_set)

class New_Lego_Set(FlaskForm):
    name = StringField("Lego Set Name", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])

    lego_bricks_id = FieldList(IntegerField("Lego brick id", validators=[DataRequired()]), min_entries=1, max_entries=100)
    lego_bricks_quantity = FieldList(IntegerField("Lego brick quantity", validators=[DataRequired()]), min_entries=1, max_entries=100)