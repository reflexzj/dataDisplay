# coding=utf-8

from dataDisplay.database import db


def init_databse(self, columns, data):
    """
    对应数据库模型类的初始化，值为每个行表中的所有值
    :param self:
    :param columns:
    :param data:
    :return:
    """
    for index in range(len(columns)):
        # 将缺省值做null处理
        if data[index]:
            value = data[index]
        else:
            value = ''
        setattr(self, columns[index], value)


class extract_data_1(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    p_id = db.Column(db.TEXT)
    p_name = db.Column(db.TEXT)
    lev = db.Column(db.TEXT)
    c_com = db.Column(db.TEXT)
    year = db.Column(db.TEXT)
    area = db.Column(db.TEXT)
    money = db.Column(db.TEXT)
    deadline = db.Column(db.TEXT)
    category = db.Column(db.TEXT)
    ks_name = db.Column(db.TEXT)
    ref_table = db.Column(db.VARCHAR(45), unique=True)

    def __repr__(self):
        return 'info:{}'.format(self.id)

    def __init__(self, columns, data):
        init_databse(self, columns, data)


def select(year, lev, area, office):
    info = None
    sel_cmd = 'info = extract_data_1.query.filter('
    if year != u'' and year != u'所有':
        year_cmd = 'extract_data_1.year == year,'
        sel_cmd += year_cmd
    if lev != u'' and lev != u'所有':
        lev_cmd = "extract_data_1.lev.like('%" + lev + "%'),"
        sel_cmd += lev_cmd
    if area != u'' and area != u'所有':
        area_cmd = "extract_data_1.area.like('%" + area + "%'),"
        sel_cmd += area_cmd
    if office != u'' and office != u'所有':
        off_cmd = 'extract_data_1.ks_name == office'
        sel_cmd += off_cmd
    sel_cmd += ').all()'
    try:
        # u_area = unicode(area)
        # info = Sheet_Form.query.filter(and_(Sheet_Form.year == year ,Sheet_Form.lev.like('%'+lev+'%'),
        #                                     Sheet_Form.area.like('%'+area+'%'),Sheet_Form.ks_name == office)).all()
        # print sel_cmd
        exec (sel_cmd)
        return info
    except IOError:
        return None
    return None
