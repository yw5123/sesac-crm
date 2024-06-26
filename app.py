from flask import Flask, render_template, redirect, url_for, request
from database import get_query
from pagefunction import get_current_page_info

app = Flask(__name__)

@app.route('/')
@app.route('/crm/users')
@app.route('/crm/users/<int:page>')
def users(page=1):
    per_page = 20
    offset = per_page * (page - 1)

    # 검색창에 입력된 값 저장
    name = request.args.get("name")
    gender = request.args.get("gender")
    age = request.args.get("age")

    # 입력된 항목 확인하고 그에 맞는 query와 params 설정
    if name and gender and age:
        query = " WHERE name LIKE ? and gender = ? and age = ?"
        params = ('%' + name + '%', gender, int(age))
    elif name and gender:
        query = " WHERE name LIKE ? and gender = ?"
        params = ('%' + name + '%', gender)
    elif name and age:
        query = " WHERE name LIKE ? and age = ?"
        params = ('%' + name + '%', int(age))
    elif gender and age:
        query = " WHERE gender = ? and age = ?"
        params = (gender, int(age))
    elif name:
        query = " WHERE name LIKE ?"
        params = ('%' + name + '%',)
    elif gender:
        query = " WHERE gender = ?"
        params = (gender,)
    elif age:
        query = " WHERE age = ?"
        params = (int(age),)
    else:
        query = ""
        params = ()

    # name의 값이 None이면 입력창에 None이 나와서 처리
    if not name:
        name = ""

    # 페이징을 위해 데이터의 개수 확인
    count_query = "SELECT COUNT(*) AS 'Num' FROM users" + query
    data_num = get_query(count_query, params)[0]['Num']

    # 검색 결과가 없는 경우 예외 처리
    if data_num == 0:
        return render_template('users.html', users="", pages="")
    
    # 페이지와 관련된 정보를 모두 받아오는 함수 - 딕셔너리로 반환
    pages = get_current_page_info(page, data_num, per_page)

    # 화면에 출력될 데이터 받아오기
    select_query = "SELECT * FROM users" + query + " LIMIT ? OFFSET ?"
    users = get_query(select_query, params + (per_page, offset))

    return render_template('users.html', users=users, pages=pages, name=name, gender=gender, age=age)

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
    app.run(host="0.0.0.0", debug=True)