from flask import Blueprint, render_template, redirect, url_for, request, flash
from database import get_query
from pagefunction import get_current_page_info

bp = Blueprint('order', __name__, url_prefix='/crm/orders')

@bp.route('/')
@bp.route('/<int:page>')
def orders(page=1):
    per_page = 20
    offset = per_page * (page - 1)

    # 추후 검색 기능추가를 위해 작성
    query = ""
    params = ()

    # 페이징을 위해 데이터의 개수 확인
    count_query = "SELECT COUNT(*) AS 'Num' FROM orders" + query
    data_num = get_query(count_query, params)[0]['Num']

    # 페이지와 관련된 정보를 모두 받아오는 함수 - 딕셔너리로 반환
    pages = get_current_page_info(page, data_num, per_page)

    # 파라미터에 마지막페이지보다 큰 값을 넣었을 경우 예외 처리
    if page > pages['last']:
        flash('임의로 URL을 변경하지 마시오.', 'warning')
        return redirect(url_for('order.orders'))

    # 검색 결과가 없는 경우 예외 처리
    if data_num == 0:
        return render_template('order/orderlist.html', 
                               orders="", 
                               pages="")

    # 화면에 출력될 데이터 받아오기
    select_query = '''SELECT o.Id AS Id, o.OrderAt AS OrderAt, u.Name AS UserName, S.Name AS StoreName
                FROM orders o JOIN users u ON o.userid = u.id
                JOIN stores s ON o.storeid = s.id''' + query + " LIMIT ? OFFSET ?"
    orders = get_query(select_query, params + (per_page, offset))

    return render_template('order/orderlist.html', 
                           orders=orders, 
                           pages=pages)

@bp.route('/<id>')
def order_detail(id):
    query = '''SELECT o.Id AS Id, o.OrderAt AS OrderAt, o.UserId AS UserId, o.StoreId AS StoreId, u.Name AS UserName, s.Name AS StoreName
            FROM orders o JOIN users u ON o.userid = u.id
            JOIN stores s ON o.storeid = s.id WHERE o.id = ?'''
    try:
        order = get_query(query, (id,))[0]
    except IndexError:
        flash('임의로 URL을 변경하지 마시오.', 'warning')
        return redirect(url_for('order.orders'))

    query = '''SELECT i.Id AS ItemId, i.Type AS ItemType, i.Name AS ItemName, i.UnitPrice AS ItemPrice
            FROM orders o JOIN orderitems oi ON o.Id = oi.OrderId
            JOIN items i ON oi.ItemId = i.Id
            WHERE o.id = ?'''
    orderinfos = get_query(query, (id,))

    query = '''SELECT SUM(i.UnitPrice) AS Total
            FROM orders o JOIN orderitems oi ON o.Id = oi.OrderId
            JOIN items i ON oi.ItemId = i.Id
            WHERE o.id = ?'''
    total = get_query(query, (id,))[0]['Total']

    return render_template('order/orderdetail.html', 
                           order=order, 
                           orderinfos=orderinfos, 
                           total=total)