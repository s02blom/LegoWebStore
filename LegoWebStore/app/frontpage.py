from flask import (Blueprint, flash, g, render_template, request, url_for)
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, IntegerField
from wtforms.validators import DataRequired
from . import db
import mysql.connector

blueprint = Blueprint('frontpage', __name__)


@blueprint.route('/', methods=("GET", "POST"))
def index():
    print("Found / and index")
    connection = db.get_connection()
    new_order = NewOrder()
    if new_order.validate_on_submit():
        customer_sql = """
        INSERT INTO Customer (CompanyName, Country, Email) VALUES
        (%(name)s, %(country)s, %(email)s)
        """
        customer_help = {
            "name" : new_order.company_name.data,
            "country": new_order.company_country.data,
            "email": new_order.email.data
        }
        shipping_adress_sql = """
        INSERT INTO ShippingAdress (StreetAdress, PostCode, City, Country) VALUES
        (%(street)s, %(code)s, %(city)s, %(country)s)
        """
        shipping_adress_data = {
            "street": new_order.street_adress.data,
            "code": new_order.post_code.data,
            "city": new_order.city.data,
            "country": new_order.shipping_country.data
        }
        order_sql = """
        INSERT INTO `Order` (OrderDate, ShippingDate, ArrivalDate, Customer, ShippingAdress) VALUES
        (curdate(), DATE_ADD(curdate(), INTERVAL 2 DAY), DATE_ADD(curdate(), INTERVAL 7 DAY), %(customer)s, %(shipping)s )
        """
        order_content_sql = """
        INSERT INTO OrderContent (`Order`, LegoSet, Quantity) VALUES
        (%(order)s, %(lego)s, %(quantity)s)
        """
        with connection.cursor() as cursor:
            try:
                cursor.execute(customer_sql, customer_help)
                customer_id = cursor.lastrowid
                cursor.execute(shipping_adress_sql, shipping_adress_data)
                cursor.fetchall()
                shipping_id = cursor.lastrowid
                order_data = {
                    "customer": customer_id,
                    "shipping": shipping_id
                }
                cursor.execute(order_sql, order_data)
                cursor.fetchall()
                order_id = cursor.lastrowid
                for i in range(len(new_order.lego_id)):
                    order_content_data = {
                        "order" : order_id,
                        "lego": new_order.lego_id[i].data,
                        "quantity": new_order.lego_quantity[i].data
                    }
                    cursor.execute(order_content_sql, order_content_data)
            except mysql.connector.Error as err:
                print(f"Unable to complete request\n Error: {err}")
                connection.rollback()
            connection.commit()

    with connection.cursor() as cursor:
        """Get things from server"""
        cursor.execute("SELECT * from LegoSet WHERE CheckAvailability(LegoSet.id) = True;")
        available_sets = cursor.fetchall()

        cursor.execute("SELECT * from LegoSet WHERE CheckAvailability(LegoSet.id) = False;")
        unavailable_sets = cursor.fetchall()


    return render_template("frontpage.html", available_sets=available_sets, unavailable_sets=unavailable_sets, form=new_order)

class NewOrder(FlaskForm):
    company_name = StringField("Company name", validators=[DataRequired()])
    company_country = StringField("International two letter code of your country", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    street_adress = StringField("Street adress", validators=[DataRequired()])
    post_code = StringField("Post code", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    shipping_country = StringField("International two letter code of your country", validators=[DataRequired()])

    lego_id = FieldList(IntegerField("Lego set id", validators=[DataRequired()]), 
                          min_entries=1, max_entries=100)
    lego_quantity = FieldList(IntegerField("Quantity", validators=[DataRequired()]),
                              min_entries=1, max_entries=100)
