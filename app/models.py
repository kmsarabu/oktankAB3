import psycopg2
from psycopg2.extras import RealDictCursor
import os


def connect():
    rds_host = os.environ['DATABASE_HOST']
    db_user = os.environ['DATABASE_USER']
    password = os.environ['DATABASE_PASSWORD']
    db_name = os.environ['DATABASE_DB_NAME']
    port = os.environ['DATABASE_PORT']

    return psycopg2.connect(sslmode="require", host=rds_host, user=db_user, password=password, dbname=db_name, connect_timeout=10000, port=port, keepalives_interval=30)

class Product:
    def __init__(self, product_name=None):
        self.product_name = product_name

    def fetch_data(self, dbconn, sqlstmt):
        with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sqlstmt)
            return cur.fetchall()
    
    def return_items(self):
        with connect() as dbconn:
            sqlstmt = "SELECT * FROM {}".format(self.product_name)
            return self.fetch_data(dbconn, sqlstmt)

    def popular_items(self, top=5, interval=180):
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

    def add(self, productId, email, qty):
        sqlstmt = "select id from Users where email='{}'".format(email)
        if not qty:
           qty=1
        with connect() as dbconn:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sqlstmt)
                userId = dict(cur.fetchone()).get('id')
                try:
                    sqlstmt = "insert into kart(userId, ProductId, qty) values({0}, {1}, {2}) on conflict(userid, productid) do update set qty = coalesce(kart.qty,1) + EXCLUDED.qty".format(userId, productId, qty)
                    cur.execute(sqlstmt)
                    dbconn.commit()
                    msg = "Added successfully"
                except Exception as e:
                    dbconn.rollback()
                    msg = "Error Occurred"

    def getProducts(self, productList):
        productListString = ",".join([ str(x) for x in productList])
        with connect() as dbconn:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                sqlstmt = """select id as productId, name, price, img_url from apparels a where id in ({0})
                          union
                          select id as productId, name, price, img_url from fashion a where id in ({0})
                          union
                          select id as productId, name, price, img_url from bicycles a where id in ({0})
                          union
                          select id as productId, name, price, img_url from jewelry a where id in ({0})
                          """.format(productListString)
                cur.execute(sqlstmt)
                return cur.fetchall()

    def view(self, email):
        sqlstmt = "select id from Users where email='{}'".format(email)
        with connect() as dbconn:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sqlstmt)
                userId = dict(cur.fetchone()).get('id')
                sqlstmt = """select productId, name, price, img_url, coalesce(qty,1) as qty from kart k join apparels a on a.id = k.productId where userId={0}
                          union
                          select productId, name, price, img_url, coalesce(qty,1) as qty from kart k join fashion a on a.id = k.productId where userId={0}
                          union
                          select productId, name, price, img_url, coalesce(qty,1) as qty from kart k join bicycles a on a.id = k.productId where userId={0}
                          union
                          select productId, name, price, img_url, coalesce(qty,1) as qty from kart k join jewelry a on a.id = k.productId where userId={0}
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

    def update(self, productId, email, qty):
        sqlstmt = "select id from Users where email='{}'".format(email)
        with connect() as dbconn:
            with dbconn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sqlstmt)
                userId = dict(cur.fetchone()).get('id')
                try:
                    sqlstmt = "update kart set qty = {} where userId={} and productId = {}".format(qty, userId, productId)
                    cur.execute(sqlstmt)
                    dbconn.commit()
                    msg = "Removed successfully"
                except:
                    dbconn.rollback()
                    msg = "Error Occurred"


class User:
    def __init__(self, db=connect()):
        try:
           self.cursor = db.cursor(cursor_factory=RealDictCursor)
        except:
           db=connect()
           self.cursor = db.cursor(cursor_factory=RealDictCursor)
        self.db = db
        self.user = None
        self.email = None

    def add(self, fname, lname, email, password):
        sql = f"INSERT INTO Users(fname, lname, email, password) VALUES(%s,%s,%s,%s);"
        data=(fname, lname, email, password)
        try:
           cur = self.db.cursor(cursor_factory=RealDictCursor)
           cur.execute(sql, data)
        except:
           self.db=connect()
           self.cursor = self.db.cursor(cursor_factory=RealDictCursor)
           cur = self.cursor
           cur.execute(sql, data)
        self.db.commit()
        cur.close()
        self.user = lname + ", " + fname
        self.email = email

    def get(self, email):
        sql = "select fname, lname, email, id from Users where email='{}'".format(email)
        try:
           cur = self.db.cursor(cursor_factory=RealDictCursor)
           cur.execute(sql)
        except:
           self.db=connect()
           self.cursor = self.db.cursor(cursor_factory=RealDictCursor)
           cur = self.cursor
           cur.execute(sql)
        return cur.fetchall()

    def verify(self, email ,password):
        sql = "SELECT email, password FROM Users WHERE email='{}' AND password='{}'".format(email, password)
        try:
           cur = self.db.cursor(cursor_factory=RealDictCursor)
           cur.execute(sql)
        except:
           self.db=connect()
           self.cursor = self.db.cursor(cursor_factory=RealDictCursor)
           cur = self.cursor
           cur.execute(sql)
        result = cur.fetchall()
        self.db.commit()
        cur.close()
        row_count =  len(result)
        if row_count == 1 :
            return True
        else:
            return False

class Review:
    def __init__(self):
        pass

    def __repr__(self):
        pass
