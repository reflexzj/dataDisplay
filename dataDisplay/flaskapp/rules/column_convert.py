# coding=utf-8
import datetime
from dataDisplay.flaskapp.rules.methods import page_tables, show_columns

log_path = 'datadisplay/flaskapp/data/logs.txt'


def convert_table_name(xls_sheet, year_name, conditions_name, re_flag= ''):
    '''
    获取对应sheet表,所对应的mysql数据库中的表名
    :param xls_sheet:
    :return: str
    '''
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logs = open(log_path, 'a')

    # 获取英文表名
    table_names = page_tables()

    try:
        xls_name = xls_sheet.split(',')[0].strip()
        sheet_name = xls_sheet.split(',')[1].strip()
        table_name = table_names[sheet_name].strip('\n')
    except Exception,e:
        error =  '规则中定义了不存在的sheet：' + unicode(sheet_name, 'utf-8')
        table_name = ''
        logs.write(time + 'error:' +e+'('+error + ')\n')


    # 获取对应属性名:year,conditions
    columns = show_columns()

    column = columns[table_name]
    org_column = column[0]
    ref_column = column[1]

    column_ref = {}
    for index in range(len(org_column)):
        key = unicode(org_column[index], 'utf-8')
        column_ref.update({key: ref_column[index]})

    try:
        year_ref = column_ref[year_name]
    except Exception,e:
        year_ref = ''
        error =  xls_name +'.xls中的' + sheet_name + '(' + table_name + ')' + '没有对应的年份属性' + year_name
        logs.write(time + 'error:' + e + '(' + error + ')\n')


    conditions = conditions_name.split(',')
    condition_ref = []
    for condition in conditions:
        try:
            ref_name = column_ref[condition.strip()]
            condition_ref.append(ref_name)
        except Exception, e:
            print e

    condition_ref = ','.join(condition_ref)

    # 要求数据去重时的变量名
    if re_flag:
        flag_ref = column_ref[re_flag]
    else:
        flag_ref = ''

    return table_name, year_ref, condition_ref, flag_ref


if __name__ == '__main__':
    table_name, year_ref, condition_ref = convert_table_name('成果科,省设施', '认定时间', '类别')

    print table_name, year_ref, condition_ref