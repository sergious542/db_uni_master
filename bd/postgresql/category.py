import psycopg2
from config import str_connect_to_db
import hashlib,\
    datetime,\
    binascii,\
    os,\
    traceback,\
    json
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


def add_category(categorys, name_category):
    data = {str(c): categorys[c] for c in range(0, len(categorys))}

    select = '''
        INSERT INTO category (id_category, name_category, other_information_category)
        VALUES (DEFAULT , '{}', '{}')
    '''.format(name_category, json.dumps(data))
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


def get_category():
    select = '''
        select id_category, name_category, other_information_category
        from category

    '''
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return [[r[0], r[1], r[2]] for r in rows]
        except:
            traceback.print_exc()
            return -1
    return -2
