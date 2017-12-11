# coding=utf-8
from dataDisplay.flaskapp.sums_models.methods import *
from dataDisplay.flaskapp.sums_models.rules.methods import *
import datetime

log_path = 'datadisplay/flaskapp/data/source_logs.txt'
log_path2 = 'datadisplay/flaskapp/data/sums_logs.txt'

def update_db(path, xls_name):

    # 待更新excle文件，同步到数据库中
    # 获取文件中的所有的sheets，以及对应数据库中的英文表名
    all_datas, sheet_names = give_sheet(path, xls_name)
    ref_names = page_tables()
    columns = show_columns()

    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logs = open(log_path, 'a')
    logs.write(time + ': 科室数据更新结果\n')

    for sheet in sheet_names:
        logs.write('sheet:' + sheet + '\n')

        datas = all_datas[sheet]
        ref_name = ref_names[sheet]
        column = columns[ref_name][1]

        for e in datas:
            # 逐条读取单个sheet中的数据，要重新构建成二位list，直接用list函数不行
            data = []
            data.append(e)

            fail_lists = []
            fail_sums = 0
            try:
                insert(ref_name, data, column)
            except:
                # 原来表
                id = data[0]
                try:
                    update_data(ref_name, id, data, column)
                except:
                    fail_lists.append(id)
                    fail_sums += 1

        logs.write('数据上传结束！\n')
        if fail_sums:
            logs.write('有部分数据未能完成更新，序号为：' + ','.join(fail_lists) + '\n')
        else:
            logs.write('所有数据更新完成！\n')

        logs.close()

def update_sums(table_name, sums, columns):
    '''
    更新数据汇总表
    :param table_name:
    :param sums:
    :param columns:
    :return:
    '''
    logs = open(log_path2, 'a')
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logs.write(time + ': 汇总表自动统计数据更新\n')

    for e in sums:
        # 逐条读取单个sheet中的数据，要重新构建成二位list，直接用list函数不行
        data = []
        data.append(e)

        fail_lists = []
        fail_sums = 0
        try:
            insert(table_name, data, columns)
        except:
            id = data[0]
            try:
                update_data(table_name, id, data, columns)
            except:
                fail_lists.append(id)
                fail_sums += 1

    logs.write('数据上传结束！\n')
    if fail_sums:
        logs.write('有部分数据未能完成更新，序号为：' + ','.join(fail_lists) + '\n')
    else:
        logs.write('所有数据更新完成！\n')


