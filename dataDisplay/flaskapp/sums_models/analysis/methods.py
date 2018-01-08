# coding=utf-8
import xlrd
import os
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
    extract_file = {'成果科抽取.xlsx', '专利科抽取.xlsx',  '合作交流科抽取.xlsx', '法规科抽取.xlsx', '高新科抽取.xlsx', '农社科抽取.xlsx'}

    for file in extract_file:
        print file
        data = xlrd.open_workbook(os.path.join(filepath , unicode(file, 'utf-8')))
        table = data.sheets()[0]
        nrows = table.nrows
        print nrows

        for index in range(2, nrows, 4):
            column_names = []
            column_vals = []

            table_name = table.row_values(index)[1].replace('\n', '').strip()
            print(table_name)
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

            all_extract_lists.update({table_name:[column_names, column_vals]})

    return all_extract_lists





def extrat_data():
    '''
    根据整理的表头，抽取对应的信息
    :return:
    '''
    extract_dicts = extract_columns()
    for table_name, column_value in extract_dicts.iteritems():
        data_list = extract_table(table_name, column_value)


