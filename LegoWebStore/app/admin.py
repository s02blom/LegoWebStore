from flask import (Blueprint, flash, g, render_template, request, url_for)
from . import db

blueprint = Blueprint('admin', __name__)

@blueprint.route("/admin", methods=("GET", "POST"))
def index():
    print("Found admins page")
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
    GROUP BY 
        LegoSet.id
    """

    customers_sql = "SELECT * FROM Customer"

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

    return render_template("admin.html", orders=orders, customers=customers)