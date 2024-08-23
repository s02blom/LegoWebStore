from flask import (Blueprint, flash, g, render_template, request, url_for)
from . import db
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, IntegerField
from wtforms.validators import DataRequired
import mysql.connector

blueprint = Blueprint('admin', __name__)

@blueprint.route("/admin", methods=("GET", "POST"))
def index():
    print("Found admins page")
    connection = db.get_connection()
    new_lego_set = New_Lego_Set()
    new_lego_brick = New_Lego_Brick()
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
            try: 
                cursor.execute(lego_set_sql, new_lego_set_data)
                cursor.fetchall()
                lego_set_id = cursor.lastrowid
                for i in range(len(new_lego_set.lego_set_content_id)):
                    lego_set_content_data = {
                        "lego_set": lego_set_id,
                        "lego_brick": new_lego_set.lego_set_content_id[i].data,
                        "quantity": new_lego_set.lego_set_content_quantity[i].data
                    }
                    cursor.execute(lego_set_content_sql, lego_set_content_data)
                    cursor.fetchall()
            except mysql.connector.Error as err:
                print(f"Unabme to complete request\n Error: {err}")
                connection.rollback()
            connection.commit()
            
    if new_lego_brick.validate_on_submit():
        lego_brick_sql = """
        UPDATE StorageLocation 
        SET Quantity = %(quantity)s
        WHERE Id = (SELECT StorageLocation FROM LegoBrick WHERE id = %(id)s)
        """
        with connection.cursor() as cursor:
            try:
                for i in range(len(new_lego_brick.lego_brick_ids)):
                    lego_brick_data = {
                        "quantity": new_lego_brick.lego_brick_quantity[i].data,
                        "id": new_lego_brick.lego_brick_ids[i].data
                    }
                    cursor.execute(lego_brick_sql, lego_brick_data)
                    cursor.fetchall()
            except mysql.connector.Error as err:
                print(f"Unabme to complete request\n Error: {err}")
                connection.rollback()
            connection.commit()
    
    order_sql = """
    SELECT `Order`.id, `Order`.TotalSum, `Order`.Customer, ShippingAdress.StreetAdress, ShippingAdress.PostCode, ShippingAdress.City, `Order`.OrderDate, `Order`.ShippingDate, `Order`.ArrivalDate
    FROM `Order`
    CROSS JOIN ShippingAdress ON `Order`.ShippingAdress = ShippingAdress.id
    """ 
    # Because of how the data has to be structured to be able to displayed it we 
    # have to split this into two different queries. 
    order_content_sql = """
    SELECT id, LegoSet.Name, OrderContent.Quantity, TRUNCATE(OrderContent.quantity * LegoSet.price, 2)
    FROM OrderContent
        CROSS JOIN LegoSet ON OrderContent.LegoSet = LegoSet.id
    WHERE 
        `Order` = %(id)s
    """

    customers_sql = "SELECT * FROM Customer"
    lego_bricks_sql = """
    SELECT LegoBrick.Id, Dim_x, Dim_Y, Dim_Z, Colour, StorageLocation.Quantity, StorageLocation
    FROM LegoBrick
    CROSS JOIN StorageLocation ON StorageLocation = StorageLocation.id
    """
    lego_set_content_sql = """
    SELECT LegoSet, LegoSet.Name, LegoBrick, Quantity 
    FROM LegoSetContent
        CROSS JOIN LegoSet ON LegoSet = LegoSet.id
    """
    storage_location_sql = "SELECT * FROM StorageLocation"

    connection = db.get_connection()
    with connection.cursor() as cursor:
        cursor.execute(order_sql)
        orders = cursor.fetchall()
        for i in range(0, len(orders)):
            data = list(orders[i])   
            id_dict = {
                "id": data[0]
            }
            cursor.execute(order_content_sql, id_dict)
            order_content = cursor.fetchall()
            data.append(order_content)
            adress = data[3] + "\n" + data[4] + "\n" + data[5]
            data[3] = adress
            orders[i] = data    # Replace the old set with the modified list instead
        cursor.execute(customers_sql)
        customers = cursor.fetchall()
        cursor.execute(lego_bricks_sql)
        lego_bricks = cursor.fetchall()
        cursor.execute(lego_set_content_sql)
        lego_set_content = cursor.fetchall()
        cursor.execute(storage_location_sql)
        storage_location = cursor.fetchall()

    with connection.cursor() as cursor:
        """Get things from server"""
        cursor.execute("SELECT * from LegoSet WHERE CheckAvilability(LegoSet.id) = True;")
        avilable_sets = cursor.fetchall()

        cursor.execute("SELECT * from LegoSet WHERE CheckAvilability(LegoSet.id) = False;")
        unavilable_sets = cursor.fetchall()

    return render_template("admin.html", 
                           orders=orders, customers=customers, lego_bricks=lego_bricks, lego_set_content=lego_set_content, storage_location=storage_location, avilable_sets=avilable_sets, unavilable_sets=unavilable_sets, 
                           lego_set_form=new_lego_set, lego_brick_form=new_lego_brick)

class New_Lego_Set(FlaskForm):
    name = StringField("Lego Set Name", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])

    lego_set_content_id = FieldList(IntegerField("Lego brick id", validators=[DataRequired()]), min_entries=1, max_entries=100)
    lego_set_content_quantity = FieldList(IntegerField("Lego brick quantity", validators=[DataRequired()]), min_entries=1, max_entries=100)

class New_Lego_Brick(FlaskForm):
    lego_brick_ids = FieldList(IntegerField("Lego Brick id", validators=[DataRequired()]), min_entries=1, max_entries=100)
    lego_brick_quantity = FieldList(IntegerField("Quantity", validators=[DataRequired()]), min_entries=1, max_entries=100)
    