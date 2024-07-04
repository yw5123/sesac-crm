from flask import Blueprint, render_template, redirect, url_for, request, flash
from database import get_query
from pagefunction import get_current_page_info

bp = Blueprint('store', __name__, url_prefix='/crm/stores')

@bp.route('/')
@bp.route('/<int:page>')
def stores(page=1):
    per_page = 20
    offset = per_page * (page - 1)

    # 검색창에 입력된 값 저장
    name = request.args.get("name")

    # 입력된 항목 확인하고 그에 맞는 query와 params 설정
    if name:
        query = " WHERE name LIKE ?"
        params = ('%' + name + '%',)
    else:
        query = ""
        params = ()

    # name의 값이 None이면 입력창에 None이 나와서 처리
    if not name:
        name = ""
        
    # 페이징을 위해 데이터의 개수 확인
    count_query = "SELECT COUNT(*) AS 'Num' FROM stores" + query
    data_num = get_query(count_query, params)[0]['Num']

    # 페이지와 관련된 정보를 모두 받아오는 함수 - 딕셔너리로 반환
    pages = get_current_page_info(page, data_num, per_page)

    # 파라미터에 마지막페이지보다 큰 값을 넣었을 경우 예외 처리
    if pages['current'] > pages['last']:
        flash('임의로 URL을 변경하지 마시오.', 'warning')
        return redirect(url_for('store.stores'))

    # 검색 결과가 없는 경우 예외 처리
    if data_num == 0:
        return render_template('store/storelist.html', 
                               stores="", 
                               pages="", 
                               name=name)

    # 화면에 출력될 데이터 받아오기
    select_query = "SELECT * FROM stores" + query + " LIMIT ? OFFSET ?"
    stores = get_query(select_query, params + (per_page, offset))

    return render_template('store/storelist.html', 
                           stores=stores, 
                           pages=pages, 
                           name=name)

@bp.route('/<id>')
def store_detail(id):
    query = "SELECT * FROM stores WHERE id = ?"
    try:
        store = get_query(query, (id,))[0]
    except IndexError:
        flash('임의로 URL을 변경하지 마시오.', 'warning')
        return redirect(url_for('store.stores'))

    query = '''SELECT strftime('%Y-%m', o.OrderAt) AS Month, COUNT(DISTINCT o.Id) AS OrderCount, COUNT(i.Id) AS ItemCount, SUM(i.UnitPrice) AS Total
                FROM stores s JOIN orders o ON s.Id = o.StoreId
                JOIN orderitems oi ON o.Id = oi.OrderId
                JOIN items i ON oi.ItemId = i.Id
                WHERE s.id = ? GROUP BY Month'''
    orderinfos = get_query(query, (id,))

    query = '''SELECT COUNT(u.id) AS NumVisits, u.name AS Name
                FROM stores s JOIN orders o ON s.id = o.storeid
                JOIN users u ON o.userid = u.id
                WHERE s.id = ? GROUP BY u.id ORDER BY NumVisits DESC LIMIT 10'''
    userinfos = get_query(query, (id,))

    return render_template('/store/storedetail.html', 
                           store=store, 
                           orderinfos=orderinfos, 
                           userinfos=userinfos)