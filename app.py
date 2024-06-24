from flask import Flask, render_template, redirect, url_for
from database import get_query, execute_query

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('users'))

@app.route('/crm/users')
def users():
    return render_template('users.html')

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