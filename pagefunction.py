import math

def get_current_page_info(currentpage, data_num, per_page):
    # 페이지 수를 10 단위로 잘라서 페이징 (1~10, 11~20, ...)

    # 검색 결과가 없는 경우에 대한 예외 처리
    if data_num == 0:
        lastpage = 1
    else:
        lastpage = math.ceil(data_num / per_page)

    current_page_list = []
    current_10 = (currentpage - 1) // 10    # 현재 페이지의 10의 자리 수

    # 페이지 버튼에 이전/다음이 있는지 여부 확인: 있는 걸 디폴트로 설정
    prevPages = True
    nextPages = True

    # 현재 페이지가 한자리 수일 때 (이전이 없는 첫 리스트에 있을 때)
    if current_10 == 0:
        prevPages = False
        if lastpage > 10:
            for i in range(1, 11):
                current_page_list.append(i)
        else:
            for i in range(1, lastpage + 1):
                current_page_list.append(i)
                nextPages = False
    # 현재 페이지가 마지막 페이지가 있는 리스트에 있을 때
    elif current_10 == ((lastpage - 1) // 10):
        for i in range(current_10 * 10 + 1, lastpage + 1):
            current_page_list.append(i)
            nextPages = False
    # 현재 페이지가 이전/다음이 있는 중간 리스트에 있을 때
    else:
        for i in range(current_10 * 10 + 1, (current_10 + 1) * 10 + 1):
            current_page_list.append(i)

    pages = {
        'current': currentpage,
        'last': lastpage,
        'pagelist': current_page_list,
        'prevPages': prevPages,
        'nextPages': nextPages,
        'data_num': data_num
    }

    return pages


if __name__ == "__main__":
    print(get_current_page_info(31, 59, 20))