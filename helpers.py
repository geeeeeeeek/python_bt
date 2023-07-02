# -*- coding: utf-8 -*-



def get_page_list(paginator, page):

    """
    分页逻辑
    if 页数>=10:
        当前页<=5时，起始页为1
        当前页>(总页数-5)时，起始页为(总页数-9)
        其他情况 起始页为(当前页-5)
    """

    page_list = []

    if paginator.num_pages > 10:
        if page.number <= 5:
            start_page = 1
        elif page.number > paginator.num_pages - 5:
            start_page = paginator.num_pages - 9
        else:
            start_page = page.number - 5

        for i in range(start_page, start_page + 10):
            page_list.append(i)
    else:
        for i in range(1, paginator.num_pages + 1):
            page_list.append(i)

    return page_list