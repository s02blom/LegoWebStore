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

def get_connection():
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
    return g.db

def close_connection(connection):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(init_db_command)

def create_tables() ->str:
    db = get_connection()
    with db.cursor() as cursor:
        with current_app.open_resource("sql/Creating.sql", "r") as f:
            file = f.read()
            cursor.execute(file, multi=True)
        res = cursor.fetchall()
        db.commit()
        get_tables = "show tables;"
        cursor.execute(get_tables)
        tables = cursor.fetchall()
    close_connection(db)
    return tables
    

def populate_tables():
    db = get_connection()
    with db.cursor() as cursor:
        with current_app.open_resource("sql/Populate_StorageLocation.sql", "r") as f:
            file = f.read()
            cursor.execute(file, multi=True)
    close_connection(db)

@click.command("init_db")
def init_db_command():
    click.echo("Creating tables...")
    click.echo(create_tables())
    click.echo("Populating tables...")
    populate_tables()
    click.echo("Done!")