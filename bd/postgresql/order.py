import psycopg2
from config import str_connect_to_db
import hashlib,\
    datetime,\
    binascii,\
    os,\
    traceback,\
    json
from decimal import Decimal
from bd.redis.authentification import set_value_user
from bd.postgresql.product import get_product


def create_connection():
    """
    метод создания подключения к БД
    :return: или подключение или None
    """
    conn = None
    try:
        conn = psycopg2.connect(str_connect_to_db)
    except:
        print ("I am unable to connect to the database")
    return conn


def create_order(id_product,
                 id_user,
                 quantity):
    pr = get_product(id_product)
    inf = pr[4]
    inf['trademark'] = pr[5]
    print(inf)
    # p.id_product, p.article, p.name, p.price, p.other, t.title_trademark, p.description

    select = '''
        INSERT INTO orders (id_order, created_on, ref_id_user, ref_id_product, ref_id_orders_state, title_product, price, quantity, other_information)
        VALUES (DEFAULT , now(), {}, {}, 1,'{}', {},{}, '{}' )
    '''.format(id_user, id_product, pr[2], Decimal(pr[3]),quantity, json.dumps(inf))
    conn = create_connection()
    print(select)
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select)
            conn.commit()
            cur.close()
            conn.commit()
            return 0
        except:
            traceback.print_exc()
            -1
    return -2


def get_orders_user(id_user):
    select = '''
        SELECT o.id_order, o.title_product, o.quantity, o.price, o.created_on, o.date_appruve, o.ref_id_orders_state, o.other_information
        FROM orders o
        WHERE o.ref_id_user = {}
    '''.format(id_user)
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select),
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
        except:
            traceback.print_exc()
            return -1
    return -2


def get_new_orders():
    select = '''
            SELECT o.id_order, o.title_product, o.quantity, o.price, o.created_on, o.date_appruve, o.ref_id_orders_state, o.other_information
            FROM orders o
            WHERE o.ref_id_orders_state = 1
        '''
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select),
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
        except:
            traceback.print_exc()
            return -1
    return -2


def approve_order(id_order):
    select = '''
        UPDATE orders
        SET date_appruve = now(),
        ref_id_orders_state = 2
        WHERE id_order = {}
    '''.format(id_order)
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select),
            conn.commit()
            cur.close()
            conn.close()
            return 0
        except:
            traceback.print_exc()
            return -1
    return -2


def reject_order(id_order):
    select = '''
        UPDATE orders
        SET date_appruve = now(),
        ref_id_orders_state = 3
        WHERE id_order = {}
    '''.format(id_order)
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select),
            conn.commit()
            cur.close()
            conn.close()
            return 0
        except:
            traceback.print_exc()
            return -1
    return -2


def history_order():
    select = '''
               SELECT o.id_order, o.title_product, o.quantity, o.price, o.created_on, o.date_appruve, o.ref_id_orders_state, o.other_information
               FROM orders o
               WHERE o.ref_id_orders_state = 2 or o.ref_id_orders_state = 3
           '''
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select),
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows
        except:
            traceback.print_exc()
            return -1
    return -2
