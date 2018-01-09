# -*- coding: utf-8 -*-
"""main view"""
from flask import Blueprint, render_template
from flask import flash
from flask import request
from flask import session
from flask_login import login_required

from dataDisplay.extensions import csrf_protect
from dataDisplay.flaskapp.decorators import *
from dataDisplay.flaskapp.elasticsearch.my_elasticsearch import fulltext_search
from dataDisplay.flaskapp.myfunc import *
from dataDisplay.flaskapp.models import *
from dataDisplay.flaskapp.model_sums import *
from dataDisplay.flaskapp.sums.create_sums import *
from dataDisplay.flaskapp.sums_models.update import insert_db
from dataDisplay.user.forms import RegisterForm
from dataDisplay.user.models import *
from dataDisplay.user.models import Role, User
from os import path
from werkzeug.utils import secure_filename, redirect

blueprint = Blueprint('data', __name__, static_folder='../static/flaskapp')


@blueprint.route('/test')
@login_required
@minister_required
def display():
    keyword = request.args.get('keyword')
    # print keyword
    result = fulltext_search(keyword)
    # print type(result)
    lenth = result['hits']['total']
    hits = result['hits']['hits']
    print hits
    # for _ in range(lenth):

    return '你妹啊'


@blueprint.route('/summary/<string:table_name>')
@login_required
@minister_required
def table_test(table_name):
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


@blueprint.route('/catalog/<string:table_id>')
@login_required
def show_catalog(table_id):
    return render_template('flaskapp/catalog/' + table_id + '.html')


@blueprint.route('/tables/<string:table_id>')
@login_required
def show_tables(table_id):
    """show dataTables"""
    if not is_allowed(current_user.department, table_id):
        abort(401)
    info = eval(table_id).query.all()
    table_name = get_table_name(table_id)
    columns = show_columns(table_id)
    column_ch = columns[0].split(',')  # 中文名
    column_en = columns[1].split(',')  # 数据库列名
    column_0 = column_ch[1:]
    column_0.append('操作')
    column_1 = column_en[1:]
    column_1.append(column_en[0])
    columns = [column_0, column_1]
    # if table_id == 'User':
    #     tmp = []
    #     for user in info:
    #         user = user.to_dict()
    #         user['name'] = chinese_department(user[''])
    #         tmp.append(user)
    #     info = tmp
    # print columns

    return render_template('flaskapp/tables.html', info=info, columns=columns, table_name=table_name)


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
    return render_template('flaskapp/search_result.html', info=hits, columns_all=columns_all)


@blueprint.route('/tables/<string:table_id>/detail/<int:data_id>')
@clerk_required
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
@clerk_required
def update_record(table_id, data_id):
    """
    更新一条记录
    :param table_id: 表id
    :param data_id: id(主键)
    :return:
    """
    if table_id == 'User':
        if current_user.roles[0].permissions >> 2 % 2 == 0 or session['permission'] != '63':
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
@clerk_required
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
        if current_user.roles[0].permissions != 15 or session['permission'] != '63':
            abort(401)
        Role.query.filter_by(user_id=data_id).delete()
        db.session.commit()
    delet_data(table_id, data_id)
    return redirect('/tables/' + table_id)


@csrf_protect.exempt
@blueprint.route('/upload', methods=['GET', 'POST'])
@clerk_required
def upload():
    if request.method == 'POST':
        f = request.files['file']
        pa = path.join('/Users/xuxian/doing/dataDisplay/dataDisplay/static/flaskapp/tmp', f.filename)
        f.save(pa)
        department = current_user.department
        # print department
        tmp = {'department1': 'farm_socity', 'department2': 'patent', 'department3': 'law', 'department4': 'cop_ex',
               'department5': 'high_new_tec', 'department6': 'result', }
        insert_db(path='/Users/xuxian/doing/dataDisplay/dataDisplay/static/flaskapp/tmp', xls_name=f.filename,
                  ks_name=tmp[department])
        return redirect('/index')
    return render_template('flaskapp/upload.html')


@blueprint.route('/addrole')
@admin_required
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
