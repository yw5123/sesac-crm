from flask import Blueprint, render_template, url_for, request
from database import get_query
from pagefunction import get_current_page_info

bp = Blueprint('item', __name__, url_prefix='/crm/items')

@bp.route('/')
@bp.route('/<int:page>')
def items(page=1):
    per_page = 20
    offset = per_page * (page - 1)

    # 추후 검색 기능 추가를 위해 작성
    query = ""
    params = ()

    # 페이징을 위해 데이터의 개수 확인
    count_query = "SELECT COUNT(*) AS 'Num' FROM items" + query
    data_num = get_query(count_query, params)[0]['Num']

    # 페이지와 관련된 정보를 모두 받아오는 함수 - 딕셔너리로 반환
    pages = get_current_page_info(page, data_num, per_page)

    # 화면에 출력될 데이터 받아오기
    select_query = "SELECT * FROM items" + query + " LIMIT ? OFFSET ?"
    items = get_query(select_query, params + (per_page, offset))

    return render_template('item/itemlist.html', items=items, pages=pages)

@bp.route('/<id>')
def item_detail(id):
    query = "SELECT * FROM items WHERE id = ?"
    item = get_query(query, (id,))[0]

    query = '''SELECT strftime('%Y-%m', o.OrderAt) AS Month, COUNT(DISTINCT o.Id) AS OrderCount, COUNT(i.Id) AS ItemCount, SUM(i.UnitPrice) AS Total
                FROM items i JOIN orderitems oi ON i.Id = oi.ItemId
                JOIN orders o ON oi.OrderId = o.Id
                WHERE i.id = ? GROUP BY Month'''
    orderinfos = get_query(query, (id,))

    return render_template('item/itemdetail.html', item=item, orderinfos=orderinfos)