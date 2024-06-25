def get_current_page_info(currentpage, lastpage):
    current_page_list = []
    current_10 = (currentpage - 1) // 10
    prevPages = True
    nextPages = True

    if current_10 == 0:
        prevPages = False
        if lastpage > 10:
            for i in range(1, 11):
                current_page_list.append(i)
        else:
            for i in range(1, lastpage + 1):
                current_page_list.append(i)
                nextPages = False
    elif current_10 == ((lastpage - 1) // 10):
        for i in range(current_10 * 10 + 1, lastpage + 1):
            current_page_list.append(i)
            nextPages = False
    else:
        for i in range(current_10 * 10 + 1, (current_10 + 1) * 10 + 1):
            current_page_list.append(i)

    return current_page_list, prevPages, nextPages


if __name__ == "__main__":
    print(get_current_page_info(31, 59))