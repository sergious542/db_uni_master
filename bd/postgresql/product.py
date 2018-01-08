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


def get_trademarks():
    select = '''
        SELECT id_trademark, title_trademark
        FROM trademark
    '''
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select)
            return [[r[0], r[1]] for r in cur.fetchall()]
        except:
            traceback.print_exc()
            return -2
    return -1


def add_product(title,article, price,trademark, other, category, description):
    select = '''
        INSERT INTO product (id_product, name, article, price, other, is_ref, ref_id_category, ref_id_trademark, description)
        VALUES (DEFAULT , '{}', '{}',{}, '{}',FALSE, {},{} ,'{}')
    '''.format(title, article, Decimal(price),json.dumps(other),category,trademark,description)
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select)
            conn.commit()
            cur.close()
            conn.close()
            return 0
        except:
            traceback.print_exc()
            return -1
    return -2


def add_trademark(trademark):
    select = '''
        INSERT INTO trademark (id_trademark, title_trademark)
         VALUES (DEFAULT, '{}' )
    '''.format(trademark)
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select)
            conn.commit()
            cur.close()
            conn.close()
            return 0
        except:
            traceback.print_exc()
            return -1
    return -2


def get_products(category_id, offset, limit):
    select = '''
        SELECT p.id_product, p.article, p.name, p.price, p.other, t.title_trademark
        FROM category c, product p, trademark t
        WHERE p.ref_id_category = c.id_category
        AND p.ref_id_trademark = t.id_trademark
        AND c.id_category = {}
        ORDER by p.id_product
        offset {} limit {}
    '''.format(category_id,
               offset,
               limit)
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return [
                [
                    r[0],  # id
                    r[1],  # article
                    r[2],  # name
                    str(r[3]),  # price
                    r[4],  # other
                    r[5]  # trade
                ]
                for r in rows
            ]
        except:
            traceback.print_exc()
            return -1
    return -2


def get_product(id_product):
    select = '''
        SELECT p.id_product, p.article, p.name, p.price, p.other, t.title_trademark, p.description
        FROM category c, product p, trademark t
        WHERE p.ref_id_category = c.id_category
        AND p.ref_id_trademark = t.id_trademark

        AND p.id_product = {}
        ORDER by p.id_product
    '''.format(id_product)
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select)
            r = cur.fetchone()
            cur.close()
            conn.close()
            return [

                    r[0],  # id
                    r[1],  # article
                    r[2],  # name
                    str(r[3]),  # price
                    r[4],  # other
                    r[5],  # trade
                r[6]
                ]

        except:
            traceback.print_exc()
            return -1
    return -2


def find_product(category_id, select):
    select = '''
        SELECT p.id_product, p.article, p.name, p.price, p.other, t.title_trademark
        FROM category c, product p, trademark t
        WHERE p.ref_id_category = c.id_category
        AND p.ref_id_trademark = t.id_trademark
        AND c.id_category = {}
        {}
        ORDER by p.id_product

    '''.format(category_id, select)
    print(select)
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return [
                [
                    r[0],  # id
                    r[1],  # article
                    r[2],  # name
                    str(r[3]),  # price
                    r[4],  # other
                    r[5]  # trade
                ]
                for r in rows
            ]
        except:
            traceback.print_exc()
            return -1
    return -2