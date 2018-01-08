from flask import Flask,\
    request,\
    render_template,\
    redirect,\
    url_for,\
    make_response
import requests
import hashlib
from urls import url_index,\
    url_sign_in,\
    url_sign_out,\
    url_registration
from bd.redis.authentification import check_user,\
    set_value_user
from bd.postgresql.entry import sign_in as si,\
    registration_user
from bd.postgresql.city import get_citys

app = Flask(__name__)

import views.authentication.view_product
import views.incognito.view_product
import views.admin.view_category
import views.admin.view_product
import views.admin.view_orders


def create_hash_password(password):
    return hashlib.sha256(bytes(str(password), 'utf-8')).hexdigest()


def index():
    sk = request.cookies.get('session_key')
    id_user = request.cookies.get('id_user')
    answer = check_user(id_user, sk)
    if answer[0]:
        if answer[1] == 'admin':
            resp = make_response(redirect(url_for('category')))  # admin
            #pass
        else:
            resp = make_response(redirect(url_for('get_products_au')))  # user
    else:
        resp = make_response(redirect(url_for('get_products_i')))  # inkognito
    return resp
"""
'{'type': 'number', 'name': 'количество цветов'},{'type': 'checkbox', 'name': 'с зеркалом'}, {'type': 'checkbox', 'name':'с кисточками'}
тени количество цветов с зеркалом с кисточками
'{'type': 'number', 'name': 'объем'}, {'type': 'checkbox', 'name': 'крассит ли'}
шампуни объем крассит ли
{'type': 'number', 'name': 'мощность'},{'type': 'number', 'name': 'режимов'}, {'type': 'checkbox', 'name': 'функция ионизации'},{'type': 'checkbox', 'name': 'холодный поток'}
фен мощность в вт ,функция ионизации, холодный поток, количество режимов
"""


def sign_in():
    if request.method == 'POST':
        di = dict(request.form)
        login = di['login'][0]
        password = create_hash_password(di['password'][0])
        res = si(login,password)
        # print(res)
        if type(res) == list:

            if res[0] == 'user':
                #print('___user___')
                url = request.cookies.get('url')
                #print(url)
                id = request.cookies.get('id')
                #print(id)
                if url:
                    if int(id)>0:
                        resp = make_response(redirect(url_for(url+'_au', id_product=id)))
                    else:
                        resp = make_response(redirect(url_for(url+'_au')))
                else:
                    resp = make_response(redirect(url_for('get_products_au')))  # user
                resp.set_cookie('end_w', '_au')
                resp.set_cookie('session_key', res[0])
                resp.set_cookie('id_user', str(res[2]))
                set_value_user(str(res[2]), res[0], 'user')

            else:
                url = request.cookies.get('url')
                id = request.cookies.get('id')
                if url:
                    if int(id) > 0:
                        resp = make_response(redirect(url_for(url, id_product=id)))
                    else:
                        resp = make_response(redirect(url_for(url)))
                else:
                    resp = make_response(redirect(url_for('category')))  # admin
                resp.set_cookie('session_key', res[0])
                resp.set_cookie('end_w', '_i')
                resp.set_cookie('id_user', str(res[2]))
                set_value_user(str(res[2]), res[0], 'admin')

        else:
            url = request.cookies.get('url')
            id = request.cookies.get('id')
            if url:
                if int(id) > 0:
                    resp = make_response(redirect(url_for(url+'_i', id_product=id)))
                else:
                    resp = make_response(redirect(url_for(url+'_i')))
            else:
                resp = make_response(redirect(url_for('get_products_i')))  # inkognito
        print(res)
        return resp


def sign_out():
    url = request.cookies.get('url')
    # print(url)
    id = request.cookies.get('id')
    # print(id)
    if url:
        if int(id) > 0:
            resp = make_response(redirect(url_for(url + '_i', id_product=id)))
        else:
            resp = make_response(redirect(url_for(url + '_i')))
    else:
        resp = make_response(redirect(url_for('get_products_i')))  # user
    # resp = make_response(redirect(url_for('get_products_i')))  # user
    resp.set_cookie('session_key', '')
    return resp


def registration():
    if request.method == 'POST':
        di = dict(request.form)
        name = di['name'][0]
        phone = di['phone'][0]
        password = create_hash_password(di['password'][0])
        mail = di['mail'][0]
        city = di['city'][0]
        res = registration_user(mail, password, phone, name, city)
        print(res)
        if type(res) == list:
            if res[0] == 'user':
                url = request.cookies.get('url')
                # print(url)
                id = request.cookies.get('id')
                # print(id)
                if url:
                    if int(id) > 0:
                        resp = make_response(redirect(url_for(url + '_au', id_product=id)))
                    else:
                        resp = make_response(redirect(url_for(url + '_au')))
                else:
                    resp = make_response(redirect(url_for('get_products_au')))  # user
                # resp = make_response(redirect(url_for('get_products_au')))  # user
                resp.set_cookie('session_key', res[0])
                resp.set_cookie('id_user', res[1])
        else:
            resp = make_response(redirect(url_for('get_products_i')))  # inkognito
        return resp
    citys = get_citys()
    return render_template('registration.html',
                           city=citys)

app.add_url_rule(url_index, 'index', index)
app.add_url_rule(url_sign_in, 'sign_in', sign_in, methods=['POST'])
app.add_url_rule(url_sign_out, 'sign_out', sign_out)
app.add_url_rule(url_registration, 'registration', registration, methods=['POST', 'GET'])





