# coding=utf-8
import xlrd
import os
from dataDisplay.flaskapp.myfunc import *


def page_tables():
    '''
    所有excles中sheets表,在mysql中对应的表名
    :return:
    '''
    filepath = 'dataDisplay/flaskapp/data/page_table.txt'
    ref_names = {}

    for data in open(filepath , 'r'):
        data = unicode(data, 'utf-8')
        data = data.split(',')
        ref_names.update({data[0]: data[1]})

    return ref_names

def show_columns():
    """
    读取存储好的文件中所有栏目表
    :return: columsn_table字典，返回原始栏目名和对应的数据库中映射表名
    """
    data = open('datadisplay/flaskapp/data/all_tables.txt', 'r').readlines()
    columns_table = {}
    for index in range(0, len(data), 3):
        try:
            table_name = unicode(data[index].strip(), 'utf-8')
            org_columns = data[index + 1].strip().split(',')
            ref_columns = data[index + 2].strip().split(',')
            columns_table.update({table_name: [org_columns, ref_columns]})
        except Exception, e:
            print 'show_columns-----------------', table_name
            print e

    return columns_table

def give_sheet(path, xls_name):
    '''
    读取一个excels中所有的sheets的内容
    :param path:
    :param xls_name:
    :return:
    '''
    data = xlrd.open_workbook(os.path.join(path, xls_name))

    # 读取所有sheets中的内容
    all_datas = {}
    sheet_names = []

    for index in range(len(data.sheets())):
        table = data.sheets()[index]
        sheet_name = table.name
        sheet_names.append(sheet_name)
        nrows = table.nrows

        datas = read_sheet(table, 1, nrows)
        all_datas.update({sheet_name:datas})

    return  all_datas, sheet_names


def read_sheet(table, begin, end):
    '''
    根据指定的序号，读取excle中的数据，行列存放到二维数组中
    :param table:
    :param begin:
    :param end:
    :param columns: 表格对应的栏目（属性）
    :return:
    '''
    all_datas = []

    for i in range(begin, end):
        data = table.row_values(i)

        row_data = []
        for cell in data:
            content = cell
            row_data.append(content)

        all_datas.append(row_data)

    return all_datas


