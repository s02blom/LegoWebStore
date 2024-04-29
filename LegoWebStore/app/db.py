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
        connection = Kalle.connect( host = os.environ.get('DATABASE_HOST'),
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
    return connection

def close_connection(connection):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_connection)
    app.cli.add_command(init_db_command)

def init_db():
    db = get_connection()
    #db.start_transaction()
    cursor = db.cursor()
    with current_app.open_resource("throwaway.sql", "r") as f:
        print("Death and destruction")
        file = f.read()
        #cursor.execute(f.read())
    #result = cursor.fetchall()
    #print(result)
    #cursor.execute("SHOW TABLES;")
    #result = cursor.fetchall()
    #print(result)
    print(file)
    statements = file.split(";")
    #cursor.execute(file, multi=True)
    statements[1] + ";"
    statements[0] + ";"
    cursor.execute(file, multi=True)
    cursor.close()
    print("!")
    #db.commit()
    print("Life and Hope")
    close_connection(db)

@click.command("init_db")
def init_db_command():
    init_db()
    click.echo("Initilizing the database")