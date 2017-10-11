# coding=utf-8
import xlrd
import re
import os
from dataDisplay.flaskapp.myfunc import *

def get_sums_rule(filepath):
    '''
    获取每张总结表中的表头，其属性对应其他基础表中的哪些属性
    包括对应基础的表名，在该表中的年份英文名，判断条件（conditons）
    以及总结表中自身属性之间的联系
    :param filepath:
    :return:
    '''
    sums_rule = {}

    data = xlrd.open_workbook(filepath)
    table = data.sheets()[0]
    nrows = table.nrows

    for index in range(1, nrows, 8):
        re_tab_names = []
        re_year_names = []
        condition_names = []
        condition_val = []
        do_set = []
        relationships = []

        # 对应的excle的sheet表名字，以及对应的数据库table名
        names = table.row_values(index)[0].split('.')
        sheet_name = names[1]
        table_name = 'sums' + '_' + re.findall(r'\d+', names[0])[0]

        for i in range(len(table.row_values(0))):
            re_tab_names.append(table.row_values(index+2)[i])
            re_year_names.append(table.row_values(index+3)[i])
            condition_names.append(table.row_values(index+4)[i])
            condition_val.append(table.row_values(index+5)[i])
            do_set.append(table.row_values(index+6)[i])
            relationships.append(table.row_values(index+7)[i])

        # print ','.join(re_tab_names)

        sums_rule.update({table_name:[re_tab_names, re_year_names, condition_names, condition_val, do_set, relationships]})

    return sums_rule

def page_tables():
    '''
    所有excles中sheets表,在mysql中对应的表名
    :return:
    '''
    filepath = 'dataDisplay/flaskapp/data/page_table.txt'
    ref_names = {}

    for data in open(filepath , 'r'):
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
            table_name = data[index].strip()
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


if __name__ == '__main__':
    get_sums_rule('../sums/sums.xlsx')