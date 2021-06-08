import psycopg2
from psycopg2.extras import RealDictCursor
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

    def fetch_data(self, dbconn, sqlstmt):
        with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sqlstmt)
            return cur.fetchall()
    
    def return_items(self):
        with connect() as dbconn:
            sqlstmt = "SELECT * FROM {}".format(self.product_name)
            return self.fetch_data(dbconn, sqlstmt)

    def popular_items(self, top=5):
        with connect() as dbconn:
            sqlstmt = """
                      with items as (
                      select item_id, category
                      from (
                       select item_id, category, cnt, 
                              rank() over (partition by category order by cnt desc) mrank
                       from (
                        select item_id, category, count(1) as cnt
                        from orders a join order_details b 
                         on a.order_id = b.order_id and a.order_date >= now() - interval '1' day
                        group by item_id, category
                        ) t
                       ) t where mrank <= {} order by cnt desc
                      )
                      SELECT id,name,price, description,img_url,'apparels' as category
                      FROM apparels a join items i on i.item_id = a.id and i.category='apparels'
                      UNION
                      SELECT id,name,price, description,img_url,'fashion' as category
                      FROM fashion a join items i on i.item_id = a.id and i.category='fashion'
                      UNION
                      SELECT id,name, price, description,img_url,'bicycles' as category
                      FROM bicycles a join items i on i.item_id = a.id and i.category='bicycles'
                      UNION
                      SELECT id,name, price, description,img_url,'jewelry' as category
                       FROM jewelry a join items i on i.item_id = a.id and i.category='jewelry'""".format(top)
            return self.fetch_data(dbconn, sqlstmt)

    def show_all_items(self):
        results = None
        with connect() as dbconn:
            sqlstmt = """
            SELECT id,name,price, description,img_url FROM apparels
            UNION
            SELECT id,name,price, description,img_url FROM fashion
            UNION
            SELECT id,name, price, description,img_url FROM bicycles
            UNION 
            SELECT id,name, price, description,img_url FROM jewelry
            ORDER BY name
            """
            return self.fetch_data(dbconn, sqlstmt)

class User:
    def __init__(self, db=connect()):
        self.cursor = db.cursor(cursor_factory=RealDictCursor)
        self.db = db

    def add(self, fname, lname, email, password):
        sql = f"INSERT INTO Users(fname, lname, email, password) VALUES(%s,%s,%s,%s);"
        data=(fname, lname, email, password)
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql, data)
        self.db.commit()
        cur.close()

    def verify(self, email ,password):
        sql = f"SELECT email , password FROM Users WHERE email='{email}' AND password='{password}'"
        cur = self.db.cursor(cursor_factory=RealDictCursor)
        cur.execute(sql)
        result = cur.fetchall()
        self.db.commit()
        cur.close()
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