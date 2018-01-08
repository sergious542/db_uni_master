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
    url_find_user,\
    url_product_inf_inc,\
    url_add_com_inc
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

from urls import url_products_incognito


def get_products():
    res = get_category()
    res = make_response(render_template('incognito/products.html',
                           categorys=res,
                           prod_inf=url_product_inf_inc,
                           cat=url_cat,
                           prod_cat=url_product_inf_inc,
                           ))
    res.set_cookie('url', 'get_products')
    res.set_cookie('id', '-1')
    return res


def get_prod_inf(id_product):
    prod = get_p(id_product)
    comments = get_comments_product(id_product)

    view_product(id_product, request)
    res = make_response(render_template('incognito/product.html',
                           product=prod,
                           lik=url_like_dis_like,
                           comments=comments[::-1],
                           id_product=id_product))
    res.set_cookie('url', 'prod_inf')
    res.set_cookie('id', str(id_product))
    return res


def add_comment_inc(id_product):
    di = dict(request.form)
    comm = di['comment'][0]
    # id_us = request.cookies.get('id_user')
    comment(id_product, comm)
    prod = get_p(id_product)
    comments = get_comments_product(id_product)
    return render_template('incognito/product.html',
                           product=prod,
                           lik=url_like_dis_like,
                           comments=comments[::-1],
                           id_product=id_product)


app.add_url_rule(url_products_incognito, 'get_products_i', get_products)
app.add_url_rule(url_product_inf_inc + '/<id_product>', 'prod_inf_i', get_prod_inf)
app.add_url_rule(url_add_com_inc + '/<id_product>', 'add_comment_inc', add_comment_inc, methods=['POST'])