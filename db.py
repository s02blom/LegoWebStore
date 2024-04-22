import os
import mysql.connector as Kalle
from mysql.connector import errorcode

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
    connection.close()

if __name__ == "__main__":
    Anka = get_connection()
    with Anka.cursor() as cursor:
        sql = "SHOW DATABASES;"
        cursor.execute(sql)
        print(cursor.fetchall())
    close_connection(Anka)

    try:
        with Anka.cursor() as cursor:
            sql = "SHOW DATABASES;"
            cursor.execute(sql)
            print(cursor.fetchall())
    except ...:
        print("Connection closed")
    