# coding=utf-8
from dataDisplay.flaskapp.sums_models.update import *
from dataDisplay.flaskapp.readxls.methods import *

def update_db(path, xls_name):

    all_datas, sheet_names = give_sheet(path, xls_name)
    ref_names = page_tables()

    for sheet in sheet_names:
        data = all_datas[sheet]
        ref_name = ref_names[sheet]
        column = show_columns(ref_name)
        try:
            insert(ref_name, data, column)
        except:
            print ref_name, 'has been inserted'

        id = data[0]
        update_data(ref_name, id, data, column)
