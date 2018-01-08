from __init__ import app
from flask import redirect,\
    render_template,\
    url_for,\
    make_response, \
    jsonify,\
    request
from urls import url_category
from pprint import pprint
from bd.postgresql.category import add_category,\
    get_category


def category():
    if request.method == 'POST':
        di = dict(request.form)
        name_cat = di['category'][0]
        cat = [{'name': di['name_'][d],'type': di['type_'][d]} for d in range (0, len(di['name_']))]
        r = add_category(cat,name_cat)
        print(r)
    res = get_category()
    return render_template('admin/categorys.html',
                           categorys=res)


app.add_url_rule(url_category, 'category', category, methods=["POST", 'GET'])
