from flask import (Blueprint, flash, g, render_template, request, url_for)
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, IntegerField
from wtforms.validators import DataRequired
from . import db

blueprint = Blueprint('frontpage', __name__)


@blueprint.route('/', methods=("GET", "POST"))
def index():
    print("Found / and index")
    connection = db.get_connection()
    unavilable_sets = []
    new_order = NewOrder()
    if new_order.validate_on_submit():
        print(f"Company name: {new_order.company_name.data}")
        print(f"Length of lego_id: {len(new_order.lego_id)}")
        customer_sql = f"""
        INSERT INTO Customer (CompanyName, Country, Email) VALUES
        ({new_order.company_name.data}, {new_order.company_country.data}, {new_order.email.data})
        """
        get_customer_id_sql = f"SELECT Customer.id FROM Customer WHERE Customer.CompanyName = {new_order.company_name.data}"
        shipping_adress_sql = f"""
        INSERT INTO ShippingAdress (StreetAdress, PostCode, City, Country) VALUES
        ({new_order.street_adress.data}, {new_order.post_code.data}, {new_order.city.data}, {new_order.shipping_country.data})
        """
        get_shipping_adress_id_sql = f"SELECT ShippingAdress.id FROM ShippingAdress WHERE ShippingAdress.StreetAdress = {new_order.street_adress.data}"
        order_sql = """
        INSERT INTO Order (OrderDate, ShippingDate, ArrivalDate, Customer, ShippingAdress) VALUES
        (curdate(), DATE_ADD(curdate(), INTERVAL 2 DAY), DATE_ADD(curdate(), INTERVAL 7 DAY), %s, %s )
        """
        get_order_id_sql = "SELECT Order.id FROM Order WHERE Order.Customer = %s"
        order_content_sql = """
        INSERT INTO OrderContent (Order, LegoSet, Quantity) VALUES
        (%s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(customer_sql)
            cursor.fetchall()
            cursor.execute(get_customer_id_sql)
            customer_id = cursor.fetchall()
            cursor.execute(shipping_adress_sql)
            cursor.fetchall()
            cursor.execute(get_shipping_adress_id_sql)
            shipping_id = cursor.fetchall()
            cursor.execute(order_sql, shipping_id)
            cursor.fetchall()
            cursor.execute(get_order_id_sql, customer_id)
            order_id = cursor.fetchall()
            for i in enumerate(new_order.lego_id):
                print(i)
                #cursor.execute(order_content_sql, (order_id, lego_set_id, ))

    with connection.cursor() as cursor:
        """Get things from server"""
        cursor.execute("SELECT * from LegoSet")
        avilable_sets = cursor.fetchall()
    return render_template("frontpage.html", avilable_sets=avilable_sets, unavilable_sets=unavilable_sets, form=new_order)

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
