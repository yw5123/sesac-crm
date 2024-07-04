from flask import Blueprint, render_template, redirect, url_for, request, flash
from database import get_query
from pagefunction import get_current_page_info

bp = Blueprint('item', __name__, url_prefix='/crm/items')

@bp.route('/')
@bp.route('/<int:page>')
def items(page=1):
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
    count_query = "SELECT COUNT(*) AS 'Num' FROM items" + query
    data_num = get_query(count_query, params)[0]['Num']

    # 페이지와 관련된 정보를 모두 받아오는 함수 - 딕셔너리로 반환
    pages = get_current_page_info(page, data_num, per_page)

    # 파라미터에 마지막페이지보다 큰 값을 넣었을 경우 예외 처리
    if pages['current'] > pages['last']:
        flash('올바르지 않은 입력값입니다.', 'warning')
        return redirect(url_for('item.items'))

    # 검색 결과가 없는 경우 예외 처리
    if data_num == 0:
        return render_template('item/itemlist.html', 
                               items="", 
                               pages="", 
                               name=name)

    # 화면에 출력될 데이터 받아오기
    select_query = "SELECT * FROM items" + query + " LIMIT ? OFFSET ?"
    items = get_query(select_query, params + (per_page, offset))

    return render_template('item/itemlist.html', 
                           items=items, 
                           pages=pages, 
                           name=name)

@bp.route('/<id>')
def item_detail(id):
    # item 기본 정보 - 파라미터를 통해 임의의 값을 넣었을 경우에 대한 예외 처리
    query = "SELECT * FROM items WHERE id = ?"
    try:
        item = get_query(query, (id,))[0]
    except IndexError:
        flash('올바르지 않은 입력값입니다.', 'warning')
        return redirect(url_for('item.items'))

    # 해당 item의 월간 매출액
    query = '''SELECT strftime('%Y-%m', o.OrderAt) AS Month, COUNT(DISTINCT o.Id) AS OrderCount, COUNT(i.Id) AS ItemCount, SUM(i.UnitPrice) AS Total
                FROM items i JOIN orderitems oi ON i.Id = oi.ItemId
                JOIN orders o ON oi.OrderId = o.Id
                WHERE i.id = ? GROUP BY Month'''
    orderinfos = get_query(query, (id,))

    return render_template('item/itemdetail.html', 
                           item=item, 
                           orderinfos=orderinfos)