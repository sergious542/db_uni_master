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


def create_session_key(password):
    return hashlib.sha256(
        bytes(str(password)
              + str(datetime.datetime.now()),
              'utf-8'))\
        .hexdigest()


def sign_in(login, password):
    session_key = create_session_key(password)
    select_admin = '''
        SELECT id_admin
        FROM admin
        WHERE mail = '{}'
        AND hash_password = '{}'
    '''.format(login, password)
    select_user = '''
        SELECT id_users
        FROM users
        WHERE mail = '{}'
        AND password_hash = '{}'
    '''.format(login, password)
    conn = create_connection()
    print(select_admin)
    print(select_user)
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select_admin)
            res_admin = cur.fetchone()
            cur.execute(select_user)
            res_user = cur.fetchone()
            print(res_admin)
            print(res_user)
            if res_admin is None and res_user is None:
                return -3
            elif res_admin:
                set_value_user(res_admin[0],session_key,'admin')
                return ['admin', session_key, res_admin[0]]
            else:
                set_value_user(res_user[0], session_key, 'user')
                return ['user',session_key,res_user[0]]
            return 0
        except:
            traceback.print_exc()
            return -2
    return -1


def registration_user(login, password, phone, name,id_city):
    session_key = create_session_key(password)
    select_admin = '''
            SELECT id_admin
            FROM admin
            WHERE mail = '{}'
        '''.format(login)
    select_user = '''
            SELECT id_users
            FROM users
            WHERE mail = '{}'
        '''.format(login)
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select_admin)
            res_admin = cur.fetchone()

            cur.execute(select_user)
            res_user = cur.fetchone()
            if (res_admin) is None and res_user is None:
                select = '''
                    INSERT INTO users (full_name, mail, password_hash, phone, ref_id_city)
                    VALUES('{}', '{}', '{}', '{}',{}) Returning id_users
                '''.format(name,login,password,phone,id_city)
                cur.execute(select)
                id_us = cur.fetchone()[0]
                conn.commit()
                conn.close()
                set_value_user(id_us, session_key, 'user')
                return ['user', session_key, id_us]
            else:
                return -3
        except:
            traceback.print_exc()
            return -2
    return -1


def get_name_user(id_user):
    select = '''
        SELECT full_name
        FROM users
        WHERE id_users = {}
    '''.format(id_user)
    conn = create_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(select)
            r = cur.fetchone()[0]
            cur.close()
            conn.close()
            return r
        except:
            pass
    return 'incognito'
