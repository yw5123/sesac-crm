from flask import Blueprint, render_template, url_for, request
from database import get_query
from pagefunction import get_current_page_info

bp = Blueprint('user', __name__, url_prefix='/crm/users')

@bp.route('/')
@bp.route('/<int:page>')
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
        return render_template('user/userlist.html', users="", pages="")
    
    # 페이지와 관련된 정보를 모두 받아오는 함수 - 딕셔너리로 반환
    pages = get_current_page_info(page, data_num, per_page)

    # 화면에 출력될 데이터 받아오기
    select_query = "SELECT * FROM users" + query + " LIMIT ? OFFSET ?"
    users = get_query(select_query, params + (per_page, offset))

    return render_template('user/userlist.html', users=users, pages=pages, name=name, gender=gender, age=age)
