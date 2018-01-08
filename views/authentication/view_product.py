from __init__ import app
from flask import redirect,\
    render_template,\
    url_for,\
    make_response, \
    jsonify,\
    request
from urls import url_products_authentication_user,\
    url_product_category,\
    url_product_inf,\
    url_cat,\
    url_like_dis_like,\
    url_comment,\
    url_create_order,\
    url_find_user
from bd.postgresql.category import get_category
from bd.postgresql.product import get_products as gp,\
    get_product as get_p
from bd.postgresql.order import create_order as co
from bd.postgresql.product import find_product as fp
from bd.mongodb.product import add_like_user_to_product
from bd.redis.authentification import get_id_user
from bd.redis.filter import set_filter, \
    get_filter
from bd.mongodb.product import comment, \
    get_comments_product,\
    view_product,\
    add_review


def categorys():
    res = get_category()
    # print(res)
    data = get_filter(request.cookies.get('session_key'), res[1])
    # print(data)
    for r in res:
        if int(r[0]) == int(res[0][0]):
            text = ''
            text += '<form method="post" action="{}"> '.format(url_for('find_user',
                                                                       id_category=res[0][0]))
            for c in r[2]:
                try:
                    if r[2][c]['type'] != 'checkbox':
                        text += r[2][c]['name'] + ' <input type="{}" name="{}" value="{}"> '.format(r[2][c]['type'],
                                                                                                      r[2][c]['name'],
                                                                                                      data[r[2][c]['name']])
                    else:
                        if data[r[2][c]['name']]:
                            text += r[2][c]['name'] + ' <input type="{}" name="{}" checked> '.format(r[2][c]['type'],
                                                                                                       r[2][c]['name'])
                        else:
                            text += r[2][c]['name'] + ' <input type="{}" name="{}"> '.format(r[2][c]['type'],
                                                                                               r[2][c]['name'])
                except:
                    text += r[2][c]['name'] + ' <input type="{}" name="{}" > '.format(r[2][c]['type'],
                                                                                         r[2][c]['name'])
            text += ' <input type="submit" value="искать"> </form> '
            # print(text)
    res = make_response(render_template('authentication/products.html',
                           categorys=res,
                           prod_inf=url_product_inf,
                           cat=url_cat,
                           prod_cat=url_product_inf,
                           fin=data))
    res.set_cookie('url', 'get_products')
    res.set_cookie('id','-1')
    return res


def get_products(id_category):
    arr = gp(id_category,0,100)
    # print(arr)
    return jsonify(arr)


def get_prod_inf(id_product):
    prod = get_p(id_product)
    comments = get_comments_product(id_product)
    # print(comments)
    view_product(id_product, request)
    res = make_response(render_template('authentication/product.html',
                           product=prod,
                           lik=url_like_dis_like,
                           comments=comments[::-1],
                           id_product=id_product))
    res.set_cookie('url', 'prod_inf')
    res.set_cookie('id', str(id_product))
    return res


def cat(id_category):
    res = get_category()
    data = get_filter(request.cookies.get('session_key'), id_category)
    #print(data)
    for r in res:
        if int(r[0]) == int(id_category):
            text = ''
            text += '<form method="post" action="{}">'.format(url_for('find_user',
                                                                      id_category=id_category))
            for c in r[2]:
                try:
                    if r[2][c]['type'] != 'checkbox':
                        text += r[2][c]['name'] + '<input type = "{}" name = "{}" value="{}">'.format(r[2][c]['type'],
                                                                                                      r[2][c]['name'],
                                                                                                      data[r[2][c]['name']])
                    else:
                        if data[r[2][c]['name']]:
                            text += r[2][c]['name'] + '<input type = "{}" name = "{}" checked>'.format(r[2][c]['type'],
                                                                                                       r[2][c]['name'])
                        else:
                            text += r[2][c]['name'] + '<input type = "{}" name = "{}">'.format(r[2][c]['type'],
                                                                                               r[2][c]['name'])
                except:
                    text += r[2][c]['name'] + '<input type = "{}" name = "{}" > '.format(r[2][c]['type'], r[2][c]['name'])
            text += '<input type="submit" value="искать"></form>'
    arr = gp(id_category, 0, 100)

    return jsonify({'text': text, 'arr': arr})


def likes(id_product, is_like):
    # print(is_like)
    if int(is_like) == 0:
        lik = True
        text = 'лайнули'
    else:
        lik = False
        text = 'дислайкнули'
    id_user = request.cookies.get('id_user')
    #print(lik)
    add_like_user_to_product(id_product,
                             id_user,
                             lik,
                             request)
    return jsonify(text)


def add_comment(id_product):
    di = dict(request.form)
    comm = di['comment'][0]
    id_us = request.cookies.get('id_user')
    comment(id_product, comm, id_us)
    prod = get_p(id_product)
    comments = get_comments_product(id_product)[::-1]
    return render_template('authentication/product.html',
                           product=prod,
                           lik=url_like_dis_like,
                           comments=comments,
                           id_product=id_product)


def create_order(id_product):
    di = dict(request.form)
    quan = di['quantity_order'][0]
    product_quality = di['product_quality'][0]
    compliance_description = di['compliance_description'][0]
    delivery_on_time = di['delivery_on_time'][0]
    quality_of_the_price = di['quality_of_the_price'][0]
    sk = request.cookies.get('session_key')
    add_review(id_product,
               product_quality,
               compliance_description,
               delivery_on_time,
               quality_of_the_price)

    id_u = get_id_user(sk)
    r = co(id_product,id_u,quan)
    # print(r)
    return redirect(url_for('prod_inf_au',
                            id_product=id_product))


def find_user(id_category):
    # print(id_category)
    # print(request.form)
    di = dict(request.form)
    keys = list(di.keys())
    print(keys)
    select = ''
    data = {}
    for k in keys:
        if di[k][0] == 'on':
            select += "AND other ->> '{}' = 'true' ".format(k)
            data[k] = 'True'
        else:
            if di[k][0]:
                select += "AND other ->> '{}' = '{}' ".format(k, di[k][0])
                data[k] = di[k][0]
    sk = request.cookies.get('session_key')
    set_filter(sk, id_category, data)
    ans = fp(id_category, select)
    return render_template('authentication/find_product.html',
                           product=ans)


def get_orders():
    pass


app.add_url_rule(url_products_authentication_user, 'get_products_au', categorys)
app.add_url_rule(url_product_category + '/<id_category>', 'products', get_products)
app.add_url_rule(url_product_inf + '/<id_product>', 'prod_inf_au', get_prod_inf)
app.add_url_rule(url_cat + '/<id_category>', 'cat', cat)
app.add_url_rule(url_like_dis_like + '/<id_product>/<is_like>', 'like', likes)
app.add_url_rule(url_create_order + '/<id_product>', 'to_order', create_order, methods=['POST'])
app.add_url_rule(url_find_user + '/<id_category>', 'find_user', find_user, methods=['POST'])
app.add_url_rule(url_comment + '/<id_product>', 'comment', add_comment, methods=['POST'])

