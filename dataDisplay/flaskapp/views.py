# -*- coding: utf-8 -*-
"""main view"""
from flask import Blueprint, render_template, jsonify
from flask import flash
from flask import json
from flask import request
from flask import send_from_directory
from flask import session
from flask_login import login_required

from dataDisplay.extensions import csrf_protect
from dataDisplay.flaskapp.decorators import *
from dataDisplay.flaskapp.elasticsearch.my_elasticsearch import fulltext_search
from dataDisplay.flaskapp.myfunc import *
from dataDisplay.flaskapp.models import *
from dataDisplay.flaskapp.sums.create_sums import *
from dataDisplay.flaskapp.sums_models.analysis.models import *
from dataDisplay.flaskapp.sums_models.interfaces import *
from dataDisplay.flaskapp.sums_models.models import *
from dataDisplay.settings import Config
from dataDisplay.user.forms import RegisterForm
from dataDisplay.user.models import *
from os import path
from werkzeug.utils import secure_filename, redirect

blueprint = Blueprint('data', __name__, static_folder='../static/flaskapp')


# @blueprint.route('/test')
# @login_required
# def display():
# table_name = 'patent_1'
# print table_name
# info = data_by_area(table_name, '开发区')
#
# columns = show_columns(table_name)
# column_ch = columns[0].split(',')  # 中文名
# column_en = columns[1].split(',')  # 数据库列名
# column_0 = column_ch[1:]
# column_1 = column_en[1:]
# if current_user.roles[0].permissions >= 7:
#     column_0.append('操作')
#     column_1.append(column_en[0])
# columns = [column_0, column_1]
# return render_template('flaskapp/tables.html', info=info, columns=columns, table_name=table_name)


@blueprint.route('/summary/<string:table_name>')
@login_required
def table_summary(table_name):
    info = eval(table_name).query.all()
    columns = show_columns(table_name)
    column_0 = columns[0].split(',')[1:]
    column_1 = columns[1].split(',')[1:]
    columns = [column_0, column_1]
    return render_template('flaskapp/summary/' + table_name + '.html', info=info, columns=columns)


@blueprint.route('/index')
@login_required
def dashboard():
    return render_template('flaskapp/index.html')


@blueprint.route('/Chinese.json')
def get_plun_ins():
    """
    datatables国际化
    :return: 中文翻译json
    """
    data = open('dataDisplay/static/flaskapp/txt/Chinese.json', 'r').read()
    return data


@blueprint.route('/charts/<string:department>')
@login_required
def show_charts(department):
    """show charts"""
    # datas = get_chart_datas(chart_id)
    if department == 'department2':
        datas = [385, 656.5, 150, 100]
        # 获取数据
        return render_template('flaskapp/charts_2.html', datas=datas)
    if department == 'department3' or 'department1':
        datas = [16880, 38210, 34450]
        # 获取数据
        return render_template('flaskapp/charts_3.html', datas=datas)


@blueprint.route('/keshilist/<int:id>')
@login_required
def statiShow(id):
    money_lev = money_lev_k(id)
    pronum_area = pronum_area_lev(id)
    money_year_area = money_area_year_lev(id)

    # 各个年份下，各区镇的国家级别数据获取
    CountryData = []
    for i in range(13):
        CountryData.append([])

    for i in range(13):
        for j in range(12):
            CountryData[i].append(money_year_area[j][i][0])

    #各个年份下，各区镇的省级数据获取
    ProvinceData = []
    for i in range(13):
        ProvinceData.append([])

    for i in range(13):
        for j in range(12):
            ProvinceData[i].append(money_year_area[j][i][1])

    # 各个年份下，各区镇的苏州数据获取
    SuzhouData = []
    for i in range(13):
        SuzhouData.append([])

    for i in range(13):
        for j in range(12):
            SuzhouData[i].append(money_year_area[j][i][2])

    # 各个年份下，各区镇的昆山数据获取
    KunshanData = []
    for i in range(13):
        KunshanData.append([])

    for i in range(13):
        for j in range(12):
            KunshanData[i].append(money_year_area[j][i][3])

    return render_template("flaskapp/chartshow.html", info1=money_lev, info2=pronum_area, info3_1=CountryData, info3_2=ProvinceData, info3_3=SuzhouData, info3_4=KunshanData)


@blueprint.route('/tables/<string:table_id>')
@login_required
def show_tables(table_id):
    """show dataTables"""
    if not is_allowed(current_user.department, table_id):
        abort(401)
    if current_user.town != '2047':
        town = int2bin(current_user.town)
        area = []
        dic = [u'开发区', u'高新区', u'花桥', u'张浦', u'周市', u'陆家', u'巴城', u'千灯', u'淀山湖', u'锦溪', u'周庄']
        for i in range(11):
            if town[i] == 1:
                area.append(dic[i])
        info = get_area_data(table_id, area)
    else:
        info = eval(table_id).query.all()
    table_name = get_table_name(table_id)
    columns = show_columns(table_id)
    column_ch = columns[0].split(',')  # 中文名
    column_en = columns[1].split(',')  # 数据库列名
    column_0 = column_ch[1:]
    column_1 = column_en[1:]
    if current_user.roles[0].permissions >= 7:
        column_0.append('操作')
        column_1.append(column_en[0])
    columns = [column_0, column_1]
    return render_template('flaskapp/tables.html', info=info, columns=columns, table_name=table_name)


@blueprint.route('/summary_tables/<string:table_id>')
@login_required
def show_summary_tables(table_id):
    """show dataTables"""
    info = eval(table_id).query.all()
    table_name = get_table_name(table_id)
    columns = show_columns(table_id)
    column_0 = columns[0].split(',')[1:]
    column_1 = columns[1].split(',')[1:]
    columns = [column_0, column_1]
    return render_template('flaskapp/summary_tables.html', info=info, columns=columns, table_name=table_name)

@blueprint.route('/search_result')
@login_required
def search_result():
    keyword = request.args.get('keyword')
    result = fulltext_search(keyword)
    hits = result['hits']['hits']
    tmp = []
    for hit in hits:
        # print hit['_index']
        tmp.append(hit['_index'])
    tables_id = set(tmp)
    columns_all = []

    # 获取表格名与表头
    for table_id in tables_id:
        # print table_id
        if is_allowed(current_user.department, table_id):
            table_name = get_table_name(table_id)
            columns = show_columns(table_id)
            column_0 = columns[0].split(',')[1:]
            column_1 = columns[1].split(',')[1:]
            columns_all.append([table_id, table_name, column_0, column_1])
    generate_excel2(columns_all, hits)
    return render_template('flaskapp/search_result2.html', info=hits, columns_all=columns_all)


@csrf_protect.exempt
@blueprint.route('/search_result_accurate', methods=['GET', 'POST'])
@login_required
def search_result_accurate():
    if request.method == 'POST':
        var = request.values
        search_result = []
        year = var['year']
        area = var['area'].split(u'镇')[0]
        lev = var['lev'].split(u'级')[0]
        office = var['office']
        info = select(year, lev, area, office)
        for i in info:
            s_data = {
                'year': i.year,
                'id': i.p_id,
                'name': i.p_name,
                'lev': i.lev,
                'area': i.area,
                'money': i.money,
                'c_com': i.c_com,
                'office': i.ks_name
            }
            search_result.append(s_data)

        generate_excel(search_result)
        return jsonify(search_result)
    town = int2bin(current_user.town)
    return render_template('flaskapp/select.html', town=town)


@blueprint.route('/tables/<string:table_id>/detail/<int:data_id>')
@login_required
def show_detail(table_id, data_id):
    """
    展示具体数据
    :param table_id:
    :param data_id:
    :return:
    """
    if not is_allowed(current_user.department, table_id):
        abort(401)
    info = eval(table_id).query.filter(eval(table_id).id == data_id)[0]
    if table_id == 'User':
        form = RegisterForm(request.form, csrf_enabled=False)
        user = info.to_dict()
        permission = Role.query.filter(Role.user_id == data_id)[0].permissions
        update_form(user, form, permission)
        return render_template('public/change_users_info.html', form=form, info=info, data_id=data_id)
    columns = show_columns(table_id)
    column_0 = columns[0].split(',')[1:]  # 中文名
    column_1 = columns[1].split(',')[1:]  # 数据库列名
    col_name = []
    for i in range(len(column_0)):
        col_name.append([column_0[i], column_1[i]])
    return render_template('flaskapp/detailAndRevise.html', columns=col_name, info=info, table_id=table_id,
                           data_id=data_id)


@blueprint.route('/tables/<string:table_id>/update/<int:data_id>', methods=['GET', 'POST'])
@update_required
def update_record(table_id, data_id):
    """
    更新一条记录
    :param table_id: 表id
    :param data_id: id(主键)
    :return:
    """
    if table_id == 'User':
        if current_user.roles[0].permissions >> 2 % 2 == 0 or current_user.username != 'admin':
            abort(401)
        form = RegisterForm(request.form, csrf_enabled=False)
        department, permission, town = cal_permission(form)
        if form.password.data:
            password = bcrypt.generate_password_hash(form.password.data)

            new_data = [form.username.data, password, form.role_name.data, department, town]
            columns = ['username', 'password', 'name', 'department', 'town']
        else:
            new_data = [form.username.data, form.role_name.data, department, town]
            columns = ['username', 'name', 'department', 'town']
        update_data(table_id, data_id, new_data, columns)
        # 分配权限x
        user = User.query.filter(User.username == form.username.data)[0]
        role = Role(permissions=permission)
        user.roles[0] = role
        user.update()
    elif current_user.roles[0].permissions >> 2 % 2 == 0:
        abort(401)
    else:
        datas = request.args
        columns = []
        new_data = []
        for column in datas:
            columns.append(column)
            new_data.append(datas[column])
        update_data(table_id, data_id, new_data, columns)
    return redirect('/tables/' + table_id)


@blueprint.route('/tables/<string:table_id>/delete/<int:data_id>')
@delete_required
def delete_record(table_id, data_id):
    """
    删除一条记录
    :param table_id: 表id
    :param data_id: 记录id
    :return:
    """
    if current_user.roles[0].permissions >> 3 % 2 == 0 or not is_allowed(current_user.department, table_id):
        abort(401)
    if table_id == 'User':
        if current_user.roles[0].permissions >> 2 % 2 == 0 or current_user.username != 'admin':
            abort(401)
        Role.query.filter_by(user_id=data_id).delete()
        db.session.commit()
    delet_data(table_id, data_id)
    return redirect('/tables/' + table_id)


@blueprint.route('/download/<string:category>')
@login_required
def download(category):
    """
    文件下载
    :return:
    """
    directory = Config.APP_DIR + '/static/flaskapp/tmp/'
    if category == 'accurate':
        filename = current_user.username + '_search_result.xls'
    elif category == 'all':
        filename = current_user.username + '_search_result_all.xls'
    return send_from_directory(directory, filename, as_attachment=True)


@blueprint.route('/downloadTemplate')
@login_required
def download_template():
    directory = Config.APP_DIR + '/static/flaskapp/upload_template/'
    return send_from_directory(directory, 'template.zip', as_attachment=True)

@csrf_protect.exempt
@blueprint.route('/upload', methods=['GET', 'POST'])
@input_required
def upload():
    if request.method == 'POST':
        f = request.files['file']
        directory = Config.APP_DIR + '/static/flaskapp/tmp'
        pa = path.join(directory, f.filename)
        f.save(pa)
        department = current_user.department
        tmp = {'1': 'farm_socity', '2': 'patent', '4': 'law', '8': 'cop_ex',
               '16': 'high_new_tec', '32': 'result', }
        list1, list2 =insert_db(path=Config.APP_DIR + '/static/flaskapp/tmp', xls_name=f.filename,
                  ks_name=tmp[department])

        ret = {}
        ret["fail"] = list1
        ret["repeat"] = list2
        return jsonify(ret)

        # return redirect('/index')
    return render_template('flaskapp/upload.html')


@blueprint.route('/addrole')
def add_role():
    """Add a role to a user."""

    # role = Role(name='admi')
    role = Role(permissions=3)
    # role.update()
    user = User.get_by_id(6)
    if len(user.roles) == 0:
        user.roles.append(role)
    else:
        user.roles[0] = role
    user.update()
    return '123'
