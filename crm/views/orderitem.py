from flask import Blueprint, render_template, redirect, url_for, request, flash
from database import get_query
from pagefunction import get_current_page_info

bp = Blueprint('orderitem', __name__, url_prefix='/crm/orderitems')

@bp.route('/')
@bp.route('/<int:page>')
def order_items(page=1):
    per_page = 20
    offset = per_page * (page - 1)
    
    # 추후 검색 기능 추가를 위해 작성
    query = ""
    params = ()

    # 페이징을 위해 데이터의 개수 확인
    count_query = "SELECT COUNT(*) AS 'Num' FROM orderitems" + query
    data_num = get_query(count_query, params)[0]['Num']

    # 페이지와 관련된 정보를 모두 받아오는 함수 - 딕셔너리로 반환
    pages = get_current_page_info(page, data_num, per_page)

    # 화면에 출력될 데이터 받아오기
    select_query = "SELECT * FROM orderitems" + query + " LIMIT ? OFFSET ?"
    orderitems = get_query(select_query, params + (per_page, offset))

    return render_template('orderitem/orderitemlist.html', 
                           orderitems=orderitems, 
                           pages=pages)