from flask import (Blueprint, flash, g, render_template, request, url_for)
from . import db

blueprint = Blueprint('admin', __name__)

@blueprint.route("/admin", methods=("GET", "POST"))
def index():
    print("Found admins page")
    # I need a data set that contains All the data about and order, with
    # a sublist of information about the lego sets themselves. Unfortunatly I
    # belive it has to be split into two different sql statements to get the right 
    # structure in Python. ``
    order_sql = """
    SELECT `Order`.id, `Order`.TotalSum, `Order`.Customer, `Order`.ShippingAdress, `Order`.OrderDate, `Order`.ShippingDate, `Order`.ArrivalDate
    FROM `Order`
    """
    order_content_sql = """
    SELECT id, LegoSet.Name, OrderContent.Quantity, (OrderContent.quantity * LegoSet.price)
    FROM OrderContent
        CROSS JOIN LegoSet ON OrderContent.LegoSet = LegoSet.id
    WHERE 
        `Order` = %(id)s
    GROUP BY 
        LegoSet.id
    """

    connection = db.get_connection()
    with connection.cursor() as cursor:
        cursor.execute(order_sql)
        orders = cursor.fetchall()
        for data in orders:
            data = list(data)
            id_dict = {
                "id": data[0]
            }
            cursor.execute(order_content_sql, id_dict)
            kalle = cursor.fetchall()
            print(kalle)
            data.append(kalle)

    print("-----\n",orders[0])
    return render_template("admin.html", orders=orders)