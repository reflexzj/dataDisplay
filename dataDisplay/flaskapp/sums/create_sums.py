# coding=utf-8
from .update import *

def update_sums(table_name, sums, columns):
    '''
    sums对应table_name表所需要的汇总数据集合
    :param table_name:
    :param sums:
    :param columns:
    :return:
    '''
    for sum in sums:
        try:
            insert(table_name, sums, columns)
        except:
            print table_name, 'has been inserted'

        id = sum[0]
        update_data(table_name, id, sum, columns)
