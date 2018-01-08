import psycopg2
from config import str_connect_to_db
import hashlib,\
    datetime,\
    binascii,\
    os,\
    traceback
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


def get_citys():
    select = '''
        SELECT id_city, name_city
        FROM city
    '''
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select)
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return [[r[0], r[1]] for r in rows]
        except:
            return -1
    return -2