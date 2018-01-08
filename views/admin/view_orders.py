from __init__ import app
from flask import redirect,\
    render_template,\
    url_for,\
    make_response, \
    jsonify,\
    request
from urls import url_get_new_orders,\
    url_reject_order, \
    url_approve_order,\
    url_history_order
from bd.postgresql.order import get_new_orders,\
    approve_order as ao, \
    reject_order as ro,\
    history_order as ho


def new_orders():
    orders = get_new_orders()
    return render_template('admin/orders_admin.html',
                           orders=orders)


def reject_order(id_order):
    ro(id_order)
    return redirect(url_for('new_orders_admin'))


def approve_order(id_order):
    ao(id_order)
    return redirect(url_for('new_orders_admin'))


def history_order():
    ord = ho()
    return render_template('admin/orders_history.html',orders=ord)


app.add_url_rule(url_get_new_orders, 'new_orders_admin', new_orders)
app.add_url_rule(url_reject_order + '/<id_order>', 'reject_order', reject_order)
app.add_url_rule(url_approve_order + '/<id_order>', 'approve_order', approve_order)
app.add_url_rule(url_history_order, 'history_order', history_order)
