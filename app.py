from flask import Flask, render_template, redirect, url_for
from database import get_query, execute_query
from pagefunction import get_current_page_info
import math

app = Flask(__name__)

@app.route('/')
@app.route('/crm/users')
@app.route('/crm/users/<int:page>')
def users(page=1):
    per_page = 20

    query = "SELECT COUNT(*) AS 'Num' FROM users"
    data_num = get_query(query)[0]['Num']
    lastpage = math.ceil(int(data_num) / per_page)
    pages = {
        'current': page,
        'last': lastpage
    }

    pages['pagelist'], pages['prevPages'], pages['nextPages'] = get_current_page_info(page, lastpage)

    query = "SELECT * FROM users LIMIT ? OFFSET ?"
    users = get_query(query, (per_page, per_page*(page - 1)))

    return render_template('users.html', users=users, pages=pages)

@app.route('/crm/orders')
def orders():
    return render_template('orders.html')

@app.route('/crm/order_items')
def order_items():
    return render_template('orderitems.html')

@app.route('/crm/items')
def items():
    return render_template('items.html')

@app.route('/crm/stores')
def stores():
    return render_template('stores.html')

if __name__ == "__main__":
    app.run(debug=True)