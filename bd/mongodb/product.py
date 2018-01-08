from pymongo import MongoClient
import datetime
from bd.postgresql.entry import get_name_user

from config import str_connect_to_db_mongo


def create_connection():
    client = MongoClient(str_connect_to_db_mongo)
    db = client.postgres
    return db.product


def create_product(id_product):
    db = create_connection()
    db.insert_one({'id_product': id_product,
                   'views': 1,
                   'comments': [],
                   'views_detail': [],
                   'reviews': []})


def view_product(id_product, request):
    db = create_connection()
    res = db.find_one({'id_product': id_product})
    try:
        db.update({'id_product': id_product},
                  {'$set': {
                      'views': res['views'] + 1
                  }
                  })
    except:
        db.update({'id_product': id_product},
                  {'$set': {
                      'views': 0
                  }
                  })
    db.update({'id_product': id_product},
              {'$addToSet':{
                  'views_detail': {
                      "date": datetime.datetime.now(),
                      "url": request.url,
                      "values": request.values,
                      "headers": request.headers.to_wsgi_list()
                  }
              }})


def add_like_user_to_product(id_product,
                             id_user,
                             is_like,
                             request):
    db = create_connection()
    product = db.find_one({'id_product': id_product})
    print(is_like)
    if product:
        try:
            us = product[id_user]
            us['is_like'] = is_like
            db.update({'id_product': id_product},
                     {'$set': {
                         id_user: us
                     }})
        except:
            db.update({'id_product': id_product},
                      {'$set': {
                          id_user: {'is_like': is_like}
                      }})
    else:
        di = {
            'id_product': id_product,
            'views': 1,
            'comments': [],
            'views_detail':[{
                "date": datetime.datetime.now(),
                "url": request.url,
                "values": request.values,
                "headers": request.headers.to_wsgi_list()
            }],
            id_user: {
                 'is_like': is_like
             }
        }

        print(di)
        db.insert_one(di)


def comment(id_product, text, id_user=None):
    db = create_connection()
    print(id_user)
    res = db.find_one({'id_product': id_product})
    if not res:
        create_product(id_product)
        db = create_connection()

    if id_user:
        db.update({'id_product': id_product},
                  {'$addToSet': {'comments': {
                      'date': datetime.datetime.now(),
                      'text': text,
                      'name': get_name_user(id_user)}

                  }})
    else:
        db.update({'id_product': id_product},
                  {'$addToSet': {'comments': {
                      'date': datetime.datetime.now(),
                      'text': text,
                      'name': 'incognito'}

                  }})


def get_comments_product(id_product):
    db = create_connection()
    try:
        res = db.find_one({'id_product': id_product})['comments']
        rr = []
        for r in res:
            rr.append(
                [
                    r['date'],
                    r['name'],
                    r['text']
                ]
            )
        arr = sorted(rr, key=lambda x: x[1])
        ans = arr[::]
        return ans
    except:
        return []


def add_review(id_product,
               product_quality,
               compliance_description,
               delivery_on_time,
               quality_of_the_price):
    db = create_connection()
    res = db.find_one({'id_product': id_product})
    if not res:
        create_product(id_product)
        db = create_connection()
    try:
        db.update({'id_product': id_product},
                  {'$addToSet': {
                      'reviews': {
                          'product_quality': product_quality,
                          'compliance_description': compliance_description,
                          'delivery_on_time': delivery_on_time,
                          'quality_of_the_price': quality_of_the_price,
                      }
                  }
                  })
    except:

        db.update({'id_product': id_product},
                  {'$set': {
                      'reviews': [{
                          'product_quality': product_quality,
                          'compliance_description': compliance_description,
                          'delivery_on_time': delivery_on_time,
                          'quality_of_the_price': quality_of_the_price,
                      }]
                  }
                  })







