import os
import mysql.connector as Kalle
from mysql.connector import errorcode
from flask import current_app, g
import click


#connection = Kalle.connect( host = os.environ.get('DATABASE_HOST'),
#                            user = os.environ.get('DATABASE_USER'),
#                            password = os.environ.get('DATABASE_PASSWORD'),
#                            database = os.environ.get('DATABASE_DB'),
#                           port = os.environ.get('DATABASE_PORT'))

def get_connection(set_autocommit = False, user_root=False):
    if user_root:
        user = "root"
    else:
        user = os.environ.get('DATABASE_USER')
    try:
        g.db = Kalle.connect( host = os.environ.get('DATABASE_HOST'),
                                user = user,
                                password = os.environ.get('DATABASE_PASSWORD'),
                                database = os.environ.get('DATABASE_DB'),
                                port = os.environ.get('DATABASE_PORT'))
    except Kalle.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password") #Ought to be replaced with some logging tool?
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    if (set_autocommit):
        g.db.autocommit = set_autocommit
    return g.db

def close_connection(connection):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(init_db_command)

def create_tables():
    db = get_connection()
    with db.cursor() as cursor:
        with current_app.open_resource("sql/Creating.sql", "r") as f:
            file = f.read()
            for result in cursor.execute(file, multi=True):
                result.fetchall()
    close_connection(db)
    
def get_tables():
    db = get_connection()
    cur = db.cursor()
    get = "SHOW TABLES;"
    cur.execute(get)
    res = cur.fetchall()
    cur.close()
    close_connection(db)
    return res

def populate_tables():
    db = get_connection()
    population_files = ["Populate_StorageLocation.sql", 
                        "Populate_LegoBrick.sql",
                        "Populate_LegoSet.sql",
                        "Populate_Customer.sql",
                        "Populate_ShippingAdress.sql",
                        "Populate_Order.sql",
                        "Populate_LegoSetContent.sql"]
                        #"Populate_OrderContent.sql"]
    with db.cursor() as cursor:
        for file in population_files:
            with current_app.open_resource("sql/"+file, "r") as f:
                file = f.read()
                cursor.execute(file)
                cursor.fetchall()
            db.commit()
    db.commit()
    close_connection(db)

def set_log_bin_trust_function_creators(value=True):
    db = get_connection(user_root=True)
    with db.cursor() as cursor:
        sql = f"SET GLOBAL log_bin_trust_function_creators = {value};"
        cursor.execute(sql)
        cursor.fetchall()
    close_connection(db)

def add_triggers():
    pass

@click.command("init_db")
def init_db_command(): 
    
    click.echo("Creating tables...")
    create_tables()
    click.echo("Adding triggers...")
    set_log_bin_trust_function_creators(1)
    add_triggers()
    #set_log_bin_trust_function_creators(0)
    click.echo("Populating tables...")
    populate_tables()
    click.echo("Done!")
