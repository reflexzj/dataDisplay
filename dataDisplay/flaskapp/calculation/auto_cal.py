# coding=utf-8
from dataDisplay.flaskapp.readxls import methods
from dataDisplay.flaskapp.models import *

def select_table(conditions, year):
    '''
    根据excle表格中给定的规则来更新汇中表数据
    :param table_name:
    :param conditions:
    :param year:
    :return:
    '''

    # 读取对应sums中的规则
    re_tab_names = conditions[0]
    re_year_names = conditions[1]
    condition_names = conditions[2]
    condition_vals = conditions[3]
    do_set = conditions[4]
    relationships = conditions[5]

    result_nums = []
    for index in range(len(re_tab_names)):

        re_name = re_tab_names[index]
        re_year = re_year_names[index]
        condition_name =condition_names[index].split(',')
        condition_val = condition_vals[index].split(',')
        set_flag = do_set[index]

        # 判断对应属性值是否要更新
        cmd = ''
        if re_name:
            result = None
            cmd = 'result =' + re_name + '.query.filter(' + re_name + '.' + re_year + '== str(year)'

            # 判断查询时是否有额外的附加条件
            if ''.join(condition_name):
                for i in range(len(condition_name)):
                    cmd += ', ' + re_name + '.' + condition_name[i] + ".like('" + condition_val[i] + "')"
                cmd += ').all()'
            else:
                cmd += ').all()'

            print cmd
            exec(cmd)

            if set_flag:
                tmp = set()
                for i in range(len(result)):
                    exec('tmp.add(result[i].'+ set_flag + ')')
                    result_num = len(tmp)
            else:
                result_num = len(result)
        else:
            result_num = 0

        result_nums.append(result_num)

    # 有些查询的结果需要加减法处理一下
    for index in range(len(relationships)):
        rel = relationships[index]
        if rel:
            print rel
            sign = rel[0]
            column_id = int(rel[1:])
            if sign == 'm':
                result_nums[index] -= result_nums[column_id]
            elif sign == 'a':
                result_nums[index] += result_nums[column_id]

    return result_nums



if __name__ == "__main__":
    all_rules = methods.get_sums_rule('../sums/sums.xlsx')

    conditions = all_rules['sums_8']
    result = select_table('sms_8', conditions, year=2005)
    print result