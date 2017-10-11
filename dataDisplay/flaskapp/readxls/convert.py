# coding=utf-8
from dataDisplay.flaskapp.readxls.methods import page_tables,show_columns


def convert_table_name(xls_sheet, year_name, conditions_name, re_flag= ''):
    '''
    获取对应sheet表,所对应的mysql数据库中的表名
    :param xls_sheet:
    :return:
    '''
    # 获取英文表名
    table_names = page_tables()

    reflect_table = {'专利科': 'patent', '农社科': 'farm_socity', '合作交流科': 'cop_ex',
                     '法规科': 'law', '成果科': 'result', '高新科': 'high_new_tec', '总结': 'sums'}

    xls_name = xls_sheet.split(',')[0].strip()
    sheet_name = xls_sheet.split(',')[1].strip()

    table_name = table_names[sheet_name].strip('\n')

    # 获取对应属性名:year,conditions
    columns = show_columns()

    column = columns[table_name]
    org_column = column[0]
    ref_column = column[1]

    column_ref = {}
    for index in range(len(org_column)):
        column_ref.update({org_column[index]: ref_column[index]})

    year_ref = column_ref[year_name]

    conditions = conditions_name.split(',')
    condition_ref = []
    for condition in conditions:
        try:
            ref_name = column_ref[condition.strip()]
            condition_ref.append(ref_name)
        except Exception, e:
            print e

    condition_ref = ','.join(condition_ref)

    # 数据去重变量名
    if re_flag:
        flag_ref = column_ref[re_flag]

    return table_name, year_ref, condition_ref, re_flag


if __name__ == '__main__':
    table_name, year_ref, condition_ref = convert_table_name(u'成果科,省设施', u'认定时间', u'类别')

    print table_name, year_ref, condition_ref