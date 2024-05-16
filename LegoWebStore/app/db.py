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

def get_connection(set_autocommit = False):
    try:
        g.db = Kalle.connect( host = os.environ.get('DATABASE_HOST'),
                                user = os.environ.get('DATABASE_USER'),
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
    with db.cursor() as cursor:
        with current_app.open_resource("sql/Populate_StorageLocation.sql", "r") as f:
            file = f.read()
            cursor.execute(file, multi=True)
    close_connection(db)

def test_create_wo_file():
    db = get_connection()
    sql_drop_statment = "DROP TABLE IF EXISTS LegoBrick, LegoSet, StorageLocation, LegoSetContent, Customer, ShippingAdress, `Order`, OrderContent;"
    sql_create_statment = """
    CREATE TABLE StorageLocation
    (
        ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        Quantity INT,
        House VARCHAR(1),
        Section VARCHAR(2),
        Drawer INT
    );"""
    with db.cursor() as cursor:
        cursor.execute(sql_drop_statment)
        print(cursor.fetchall())
        for result in cursor.execute(sql_create_statment, multi=True):
            print(result.fetchall())
        cursor.execute("SHOW tables;")
        print(cursor.fetchall())
    close_connection(db)

@click.command("init_db")
def init_db_command():
    click.echo("Creating tables...")
    click.echo(f"Before: {get_tables()}")
    click.echo(create_tables())
    #click.echo(test_create_wo_file())
    click.echo(f"After {get_tables()}")
    click.echo("Populating tables...")
    populate_tables()
    click.echo("Done!")