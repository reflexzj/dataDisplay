# -*- coding: utf-8 -*-
"""
# @Time    :2017/9/7 下午3:23
# @Author  :Xuxian
"""


def get_chart_datas(chart_id):
    pass


def show_columns(table_id):
    """
    读取存储好的文件中所有栏目表
    :return: columsn_table字典，返回原始栏目名和对应的数据库中映射表名
    """
    data = open('dataDisplay/static/flaskapp/txt/all_tables.txt', 'r').readlines()
    columns_table = {}
    for index in range(0, len(data), 3):
        try:
            table_name = data[index].strip()
            org_columns = data[index + 1].strip()
            ref_columns = data[index + 2].strip()
            columns_table.update({table_name: [org_columns, ref_columns]})
        except Exception, e:
            print 'show_columns-----------------', table_name
            print e

    return columns_table[table_id]


def get_table_name(name):
    """
    读取数据库表名对应的中文名
    :param name:
    :return: string 表名
    """

    data = open('dataDisplay/static/flaskapp/txt/page_table.txt', 'r').readlines()
    for lis in data:
        tmp = lis.split(',')
        if tmp[1].strip() == name:
            return tmp[0].strip()
    return


def is_allowed(department, table_id):
    dic = {'department1': 'farm_socity',
           'department2': 'petent',
           'department3': 'law',
           'department4': 'cop_ex',
           'department5': 'high_new_tec',
           'department6': 'result',
           }
    print dic[department]
    lenth = len(dic[department])
    if table_id[:lenth] == dic[department]:
        return True
    return False


def myfunc(a, n, k):
    global sum

    if n == 1:
        b = 0

        for j in range(len(a) - 1):
            if a[j] < a[j + 1]:
                b += 1

        if b == k:
            sum += 1
    else:
        for i in range(n):
            # print i
            a[i], a[n - 1] = a[n - 1], a[i]
            myfunc(a, n - 1, k)
            a[n - 1], a[i] = a[i], a[n - 1]


if __name__ == '__main__':
    input = raw_input().strip().split()
    n = int(input[0])
    k = int(input[1])
    list = []
    for i in range(n):
        list.append(i + 1)
    sum = 0
    myfunc(list, n, k)
    print sum
