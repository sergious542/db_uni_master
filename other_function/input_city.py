import xlrd
import psycopg2
from config import str_connect_to_db


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


def read_file():
    rb = xlrd.open_workbook('../other/ukr.xls', formatting_info=True)

    # выбираем активный лист
    sheet = rb.sheet_by_index(0)
    # val = sheet.row_values(1)[0]
    conn = create_connection()
    cur = conn.cursor()
    for rownum in range(1,sheet.nrows):
        r = sheet.row_values(rownum)
        select = """
            SELECT add_city_region('{}','{}')
        """.format(r[0], r[1])
        cur.execute(select)
        conn.commit()
    select = """
        SELECT set_root_city('Черновцы','Черновицкая область');
        SELECT set_root_city('Чернигов','Черниговская область');
        SELECT set_root_city('Черкассы','Черкасская область');
        SELECT set_root_city('Хмельницкий','Хмельницкая область');
        SELECT set_root_city('Херсон','Херсонская область');
        SELECT set_root_city('Харьков','Харьковская область');
        SELECT set_root_city('Тернополь','Тернопольская область');
        SELECT set_root_city('Сумы', 'Сумская область');
        SELECT set_root_city('Ровно', 'Ровненская область');
        SELECT set_root_city('Полтава','Полтавская область');
        SELECT set_root_city('Одесса', 'Одесская область');
        SELECT set_root_city('Львов', 'Львовская область');
        SELECT set_root_city('Кировоград', 'Кировоградская область');
        SELECT set_root_city('Луганск', 'Луганская область');
        SELECT set_root_city('Киев', 'Киевская область');
        SELECT set_root_city('Ивано-Франковск', 'Ивано-Франковская область');
        SELECT set_root_city('Запорожье', 'Запорожская область');
        SELECT set_root_city('Ужгород', 'Закарпатская область');
        SELECT set_root_city('Житомир', 'Житомирская область');
        SELECT set_root_city('Донецк', 'Донецкая область');
        SELECT set_root_city('Днепропетровск', 'Днепропетровская область');
        SELECT set_root_city('Луцк', 'Волынская область');
        SELECT set_root_city('Винница', 'Винницкая область');
        SELECT set_root_city('Симферополь', 'Автономная Республика Крым');
    """
    cur.execute(select)
    conn.commit()
    cur.close()
    conn.close()

read_file()

