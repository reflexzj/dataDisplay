# coding=utf-8
from dataDisplay.flaskapp.sums_models.methods import *
from methods import *
from dataDisplay.flaskapp.sums_models.methods import *

def extrat_data():
    '''
    根据整理的表头，抽取对应的信息,存入extract_data_1中去
    :return:
    '''
    extract_dicts = extract_columns()

    for table_name, column_value in extract_dicts.iteritems():
        data_list = extract_table(table_name, column_value)
        columns = 'p_id,p_name,lev,c_com,year,area,money,deadline,category,ks_name,ref_table'
        columns = columns.split(',')
        fail_lists = insert('extract_data_1', data_list, columns)
        print('\n'.join(fail_lists))

        # print('------', table_name, '------')
        # for data in data_list:
        #     print ','.join(data)
