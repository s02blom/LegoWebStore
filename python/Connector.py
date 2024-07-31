import os
import mysql.connector as Kalle


connection = Kalle.connect( host = os.environ.get('DATABASE_HOST'),
                            user = os.environ.get('DATABASE_USER'),
                            password = os.environ.get('DATABASE_PASSWORD'),
                            database = os.environ.get('DATABASE_DB'),
                            port = os.environ.get('DATABASE_PORT'))

with connection:
    with connection.cursor() as cursor:
        sql = "SHOW DATABASES;"
        cursor.execute(sql)
        print(cursor.fetchall())
        #sql = "USE example;"
        #cursor.execute(sql)
        sql = "SHOW TABLES;"
        cursor.execute(sql)
        print(cursor.fetchall())
        # sql = """CREATE TABLE IF NOT EXISTS guestbook (
        #     id MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        #     visitor_name VARCHAR(255) NOT NULL,
        #     note TEXT NULL,
        #     created_at DATETIME DEFAULT now()
        #     );"""
        #cursor.execute(sql)
        sql = "Select * from LegoSet;"
        cursor.execute(sql)
        lego_set = cursor.fetchall()
        for set in lego_set:
            print(set)
        print(lego_set)
        print(cursor.fetchall())