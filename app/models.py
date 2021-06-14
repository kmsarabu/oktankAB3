import psycopg2
from psycopg2.extras import RealDictCursor
import os


def connect():
    rds_host = os.environ['DATABASE_HOST']
    db_user = os.environ['DATABASE_USER']
    password = os.environ['DATABASE_PASSWORD']
    db_name = os.environ['DATABASE_DB_NAME']
    port = os.environ['DATABASE_PORT']

    return psycopg2.connect(sslmode="require", host=rds_host, user=db_user, password=password, dbname=db_name, connect_timeout=10000, port=port)

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

    def popular_items(self, top=5, interval=7):
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
                         on a.order_id = b.order_id and a.order_date >= now() - interval '{0}' day
                        group by item_id, category
                        ) t
                       ) t where mrank <= {1} order by cnt desc
                      )
                      SELECT id,name,price, description,img_url,'apparels' as category, count(1) review_cnt, round(avg(rating)*20) rating
                      FROM apparels a join items i on i.item_id = a.id and i.category='apparels'
                       left outer join reviews r on r.category='apparels' and i.item_id = r.item_id
                      GROUP BY id,name,price, description,img_url
                      UNION
                      SELECT id,name,price, description,img_url,'fashion' as category, count(1) review_cnt, round(avg(rating)*20) rating
                      FROM fashion a join items i on i.item_id = a.id and i.category='fashion'
                       left outer join reviews r on r.category='fashion' and i.item_id = r.item_id
                      GROUP BY id,name,price, description,img_url
                      UNION
                      SELECT id,name, price, description,img_url,'bicycles' as category, count(1) review_cnt, round(avg(rating)*20) rating
                      FROM bicycles a join items i on i.item_id = a.id and i.category='bicycles'
                       left outer join reviews r on r.category='bicycles' and i.item_id = r.item_id
                      GROUP BY id,name,price, description,img_url
                      UNION
                      SELECT id,name, price, description,img_url,'jewelry' as category, count(1) review_cnt, round(avg(rating)*20) rating
                       FROM jewelry a join items i on i.item_id = a.id and i.category='jewelry'
                       left outer join reviews r on r.category='jewelry' and i.item_id = r.item_id
                      GROUP BY id,name,price, description,img_url
                       """.format(interval, top)
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

class Kart:
    def __init__(self):
        pass

    def add(self, productId, email):
        sqlstmt = "select id from Users where email='{}'".format(email)
        with connect() as dbconn:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sqlstmt)
                userId = dict(cur.fetchone()).get('id')
                try:
                    sqlstmt = "insert into kart(userId, ProductId) values({}, {})".format(userId, productId)
                    cur.execute(sqlstmt)
                    dbconn.commit()
                    msg = "Added successfully"
                except:
                    dbconn.rollback()
                    msg = "Error Occurred"

    def view(self, email):
        sqlstmt = "select id from Users where email='{}'".format(email)
        with connect() as dbconn:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sqlstmt)
                userId = dict(cur.fetchone()).get('id')
                sqlstmt = """select productId, name, price, img_url from kart k join apparels a on a.id = k.productId where userId={0}
                          union
                          select productId, name, price, img_url from kart k join fashion a on a.id = k.productId where userId={0}
                          union
                          select productId, name, price, img_url from kart k join bicycles a on a.id = k.productId where userId={0}
                          union
                          select productId, name, price, img_url from kart k join jewelry a on a.id = k.productId where userId={0}
                          """.format(userId)
                cur.execute(sqlstmt)
                return cur.fetchall()

    def remove(self, productId, email):
        sqlstmt = "select id from Users where email='{}'".format(email)
        with connect() as dbconn:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sqlstmt)
                userId = dict(cur.fetchone()).get('id')
                try:
                    sqlstmt = "delete from kart where userId={} and productId = {}".format(userId, productId)
                    cur.execute(sqlstmt)
                    dbconn.commit()
                    msg = "Removed successfully"
                except:
                    dbconn.rollback()
                    msg = "Error Occurred"

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

    def get(self, email):
        sql = "select fname, lname, email, id from Users where email='{}'".format(email)
        with self.db.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            return cur.fetchall()

    def verify(self, email ,password):
        sql = "SELECT email, password FROM Users WHERE email='{}' AND password='{}'".format(email, password)
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
