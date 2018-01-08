from __init__ import app
from flask import redirect,\
    render_template,\
    url_for,\
    make_response, \
    jsonify,\
    request
from urls import url_add_product,\
    url_add_trademark
from pprint import pprint
from bd.postgresql.category import add_category,\
    get_category
from bd.postgresql.product import get_trademarks,add_product as ap,\
    add_trademark as at


def add_product(id_category):
    cat = get_category()
    c = None
    for ca in cat:
        if int(id_category) == int(ca[0]):
            c = ca
    if request.method == 'POST':
        di = dict(request.form)
        title = di['title'][0]
        article = di['article'][0]
        price = di['price'][0]
        trademark = di['trademark'][0]
        description = di['description'][0]
        data = {}
        for ca in c[2]:
            try:
                if c[2][ca]['type'] == 'checkbox':
                    try:
                        a = di[c[2][ca]['name']][0]
                        data[c[2][ca]['name']] = True
                    except:
                        data[c[2][ca]['name']] = False
                else:
                    data[c[2][ca]['name']] = di[c[2][ca]['name']][0]
            except:
                data[c[2][ca]['name']] = ''

        ap(title, article, price, trademark, data, id_category, description)
    tr = get_trademarks()
    return render_template('admin/product_new.html',
                           cat=c,
                           tra=tr, id_cat=id_category)


def add_trademark():
    if request.method == 'POST':
        di = dict(request.form)
        trademark = di['trademark'][0]
        at(trademark)
    tr = get_trademarks()
    return render_template('admin/trademark.html', tra=tr)


app.add_url_rule(url_add_product + '/<id_category>','add_product', add_product, methods=['POST', 'GET'])
app.add_url_rule(url_add_trademark, 'add_trademark', add_trademark, methods=['POST', 'GET'])