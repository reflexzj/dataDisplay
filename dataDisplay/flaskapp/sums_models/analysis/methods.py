# coding=utf-8
'''
    1.读取待抽取表头，并生成对应的英文索引
'''

import xlrd
import os
import re
from dataDisplay.flaskapp.sums_models.rules.methods import page_tables, convert_column

def extract_columns():
    '''
    读取科室清单表目录，建立对应的联系
    :return:
    '''
    all_extract_lists = {}

    # 数据库中所有表的英文名对照表
    all_table_names = page_tables()

    filepath = 'dataDisplay/flaskapp/sums_models/analysis/extract'
    extract_file = {'成果科抽取.xlsx',
                    '专利科抽取.xlsx',
                    '合作交流科抽取.xlsx',
                    '法规科抽取.xlsx',
                    '高新科抽取.xlsx',
                    '农社科抽取.xlsx'}

    for file in extract_file:
        # print file
        ks_name = unicode(file.replace('抽取.xlsx', ''), 'utf-8')
        data = xlrd.open_workbook(os.path.join(filepath , unicode(file, 'utf-8')))
        table = data.sheets()[0]
        nrows = table.nrows

        for index in range(2, nrows, 4):
            column_names = []
            column_vals = []

            table_name = table.row_values(index)[1].replace('\n', '').strip()
            # print(table_name)
            table_name = all_table_names[table_name].strip('\n')

            # 将规则中的各类数据中文名映射成对应的英文
            column_ref = convert_column(table_name)

            for i in range(1, len(table.row_values(index + 1))):
                column_name = table.row_values(index + 1)[i].strip()
                try:
                    column_val = table.row_values(index + 2)[i].strip()
                except:
                    column_val=''

                # 将对应中文表头转换为英文表头，多个之间用’,‘隔开
                column_name_ref = []
                if  column_name.strip():
                    column_name = column_name.split(',')
                    for column in column_name:
                        try:
                            column = column_ref[column]
                            column_name_ref.append(column)
                        except:
                            print table_name, column
                            column_name = ''
                    column_name = ','.join(column_name_ref)
                else:
                    column_name = ''

                column_names.append(column_name)
                column_vals.append(column_val)

            all_extract_lists.update({table_name:[column_names, column_vals, ks_name]})

    return all_extract_lists


def data_pro(index, data, value):
    '''
    根据不同的格式，处理不同的数据
    :param index:p_id,p_name,lev,c_com,year,area,money,deadline,category,
    :param data:
    :return:
    '''
    try:
        if index ==2:
            if data:
                if unicode('省','utf-8') in data:
                    data = '省级'
                elif unicode('苏','utf-8') in data:
                    data = '苏州'
                elif unicode('昆','utf-8') in data:
                    data = '昆山'
                else:
                    data = '国家'
                # print data
        elif index == 4:
            data  = judge_year(re.findall('\d+', data))[0]
            if len(data) == 2:
                if int(data) > 50:
                    data = '19' + data
                else:
                    data = '20' + data
        elif index == 7:
            data = judge_year(re.findall('\d+', data.replace(r'.\d*', '')))[-1]
            if len(data) == 2:
                if int(data) > 50:
                    data = '19' + data
                else:
                    data = '20' + data
        elif index == 6:
            data = float(re.findall('\d+\.?\d*', data)[0])
            if value:
                data = str(data/10000)
            else:
                data = str(data)
        else:
            data = data.replace(' ', '').replace('\n', '')
    except Exception,e:
        if data:
            print index,'missing_value',data
            print e

    return  data

def judge_year(datas):
    new_datas = []
    for data in datas:
        if len(data) == 2 or len(data) == 4:
            new_datas.append(data)

    return new_datas

