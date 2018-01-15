# -*- coding: utf-8 -*-
"""
# @Time    :2017/9/7 下午3:23
# @Author  :Xuxian
"""

import xlwt
from flask.ext.login import current_user

from dataDisplay.settings import Config


def get_chart_datas(chart_id):
    pass


def get_table_datas(table_id):
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
    try:
        dic = {'farm': 0b000001,
               'pate': 0b000010,
               'law_': 0b000100,
               'cop_': 0b001000,
               'high': 0b010000,
               'resu': 0b100000,
               'User': 0b111111,
               }
        permission = dic[table_id[:4]]
        if permission & int(department) == permission:
            return True
        return False
    except:
        return False


def int2bin(x):
    arr = bytearray(bin(int(x)))[2:]
    tmp = []
    for byte in arr:
        tmp.append(byte - 48)
    length = 11 - len(tmp)
    [tmp.insert(0, 0) for _ in range(length)]
    return tmp


def update_form(user, form, permission):
    department = int2bin(user['department'])
    for i in range(1, 7):
        depart = 'department' + str(i)
        form[depart].data = department[-i]

    operation = int2bin(permission)
    form.output.data = operation[-1]
    form.input.data = operation[-2]
    form.update.data = operation[-3]
    form.delete.data = operation[-4]

    if user['town'] == '2047':
        form.town_all.data = 1
    else:
        towns = int2bin(user['town'])
        for i in range(1, 12):
            town = 'town' + str(i)
            form[town].data = towns[-i]
    return form


def cal_permission(form):
    department = (1 if form.department1.data == True else 0) + (2 if form.department2.data == True else 0) + (
        4 if form.department3.data == True else 0) + (8 if form.department4.data == True else 0) + (
                     16 if form.department5.data == True else 0) + (32 if form.department6.data == True else 0)
    permission = (1 if form.output.data == True else 0) + (2 if form.input.data == True else 0) + (
        4 if form.update.data == True else 0) + (8 if form.delete.data == True else 0)
    if form.town_all.data:
        town = 2047
    else:
        town = (1 if form.town1.data == True else 0) + (2 if form.town2.data == True else 0) + (
            4 if form.town3.data == True else 0) + (8 if form.town4.data == True else 0) + (
                   16 if form.town5.data == True else 0) + (32 if form.town6.data == True else 0) + (
                   64 if form.town7.data == True else 0) + (128 if form.town8.data == True else 0) + (
                   256 if form.town9.data == True else 0) + (512 if form.town10.data == True else 0) + (
                   1024 if form.town11.data == True else 0)
    return department, permission, town


def generate_excel(data):
    title = ["年度", "项目编号", "项目名称", "级别", "区镇", "经费(万元)", "截止时间", "科室"]
    book = xlwt.Workbook(encoding='utf-8')  # 创建一个excel对象
    sheet = book.add_sheet('Sheet1', cell_overwrite_ok=True)  # 添加一个sheet页
    key = ["year", "id", "name", "lev", "area", "money", "deadline", "office", ]
    for i in range(len(title)):
        sheet.write(0, i, title[i])
    for i in range(0, len(data)):
        for j in range(len(title)):
            sheet.write(i + 1, j, data[i][key[j]])
    filename = Config.APP_DIR + '/static/flaskapp/tmp/' + current_user.username + '_search_result.xls'
    book.save(filename)


def generate_excel2(columns_all, data):
    book = xlwt.Workbook(encoding='utf-8')  # 创建一个excel对象
    sheet = book.add_sheet('Sheet1', cell_overwrite_ok=True)  # 添加一个sheet页
    i = 0
    for columns in columns_all:
        table_id = columns[0]
        table_name = columns[1]
        column_0 = columns[2]
        column_1 = columns[3]
        sheet.write(i, 0, table_name)  # 表名
        i += 1
        j = 0
        for name in column_0:  # 表头
            sheet.write(i, j, name)
            j += 1
        i += 1
        for line in data:  # 数据
            if line['_index'] == table_id:
                tmp = line['_source']
                for j in range(len(column_1)):
                    try:
                        # print tmp[column_1[j]]
                        sheet.write(i, j, tmp[column_1[j]])
                    except:
                        pass
                i += 1
        i += 1
    filename = Config.APP_DIR + '/static/flaskapp/tmp/' + current_user.username + '_search_result_all.xls'
    book.save(filename)


# class ChineseTokenizer(Tokenizer):
#     """
#     全文搜索中文分词器
#     """
#
#     def __call__(self, value, positions=False, chars=False,
#                  keeporiginal=False, removestops=True,
#                  start_pos=0, start_char=0, mode='', **kwargs):
#         assert isinstance(value, jieba.text_type), "%r is not unicode" % value
#         t = Token(positions, chars, removestops=removestops, mode=mode,
#                   **kwargs)
#         seglist = jieba.cut(value, cut_all=False)  # 使用结巴分词库进行分词
#         for w in seglist:
#             t.original = t.text = w
#             t.boost = 1.0
#             if positions:
#                 t.pos = start_pos + value.find(w)
#             if chars:
#                 t.startchar = start_char + value.find(w)
#                 t.endchar = start_char + value.find(w) + len(w)
#             print t
#             yield t  # 通过生成器返回每个分词的结果token
#
#
# def ChineseAnalyzer():
#     return ChineseTokenizer()
#


if __name__ == '__main__':
    print int2bin(1023)
