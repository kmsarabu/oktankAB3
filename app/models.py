import pymysql
import psycopg2
import os


def connect():
    rds_host = os.environ['DATABASE_HOST']
    db_user = os.environ['DATABASE_USER']
    password = os.environ['DATABASE_PASSWORD']
    db_name = os.environ['DATABASE_DB_NAME']
    port = os.environ['DATABASE_PORT']

    return psycopg2.connect(host=rds_host, user=db_user, password=password, dbname=db_name, connect_timeout=10000, port=port)

class Product:
    def __init__(self, product_name=None):
        self.product_name = product_name
        print("cursor connection done!!!")

    
    def return_items(self):
        products = None
        with connect() as dbconn:
            with dbconn.cursor() as cur:
                return cur.execute("SELECT * FROM {}".format(self.product_name)).fetchall()

    def show_all_items(self):
        results = None
        with connect() as dbconn:
            with dbconn.cursor() as cur:
                sql = """
                SELECT id,name,price, description,img_url FROM apparels
                UNION
                SELECT id,name,price, description,img_url FROM fashion
                UNION
                SELECT id,name, price, description,img_url FROM bicycles
                UNION 
                SELECT id,name, price, description,img_url FROM jewelry
                ORDER BY name
                """
                return cur.execute(sql).fetchall()

class User:
    def __init__(self, db=connect()):
        self.cursor = db.cursor()
        self.db = db

    def add(self, fname, lname, email, password):
        sql = f"INSERT INTO User(fname, lname, email, password) VALUES(?,?,?,?)"
        data=(fname, lname, email, password)
        cur = self.cursor
        cur.execute(sql, data)
        self.db.commit()
        cur.close()
        self.db.close()
        

    def verify(self, email ,password):
        sql = f"SELECT email , password FROM User WHERE email='{email}' AND password='{password}'"
        cur = self.cursor
        cur.execute(sql)
        result = cur.fetchall()
        self.db.commit()
        cur.close()
        self.db.close()
        row_count =  len(result)
        print(row_count)
        if row_count == 1 :
            return True
        else:
            return False

class Review:
    def __init__(self):
        pass

    def __repr__(self):
        pass
