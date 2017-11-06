from dataDisplay.flaskapp.rules import sums_rules
from dataDisplay.flaskapp.calculation.auto_cal import select_table


def sums_update(table_name, start_y, end_y):
    all_rules = sums_rules.get_sums_rule('datadisplay/flaskapp/data/newsums.xlsx')
    conditions = all_rules[table_name]

    datas = []
    for year in range(start_y, end_y+1):
        data = select_table(conditions, year)
        datas.append(data)