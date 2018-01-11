# coding=utf-8

from dataDisplay.database import db
from sqlalchemy import or_, and_

def init_databse(self, columns, data):
    """
    对应数据库模型类的初始化，值为每个行表中的所有值
    :param self:
    :param columns:
    :param data:
    :return:
    """
    for index in range(len(data)):
        # 将缺省值做null处理
        if str(data[index]).strip():
            value = data[index]
        else:
            value = None
        setattr(self, columns[index], value)

class Sheet_Form(db.Model):
    __tablename__ = 'extract_data_1'
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
    ref_table = db.Column(db.TEXT)

    def __repr__(self):
        return '<Sheet_Form {}'.format(self.p_name)


def select(year, lev, area, office):
    sel_cmd = 'info = Sheet_Form.query.filter(and_('
    if year != u'' and year != u'所有':
        year_cmd = 'Sheet_Form.year == year,'
        sel_cmd += year_cmd
    if lev != u'' and lev != u'所有':
        lev_cmd = "Sheet_Form.lev.like('%" + lev + "%'),"
        sel_cmd += lev_cmd
    if area != u'' and area != u'所有':
        area_cmd = "Sheet_Form.area.like('%" + area + "%'),"
        sel_cmd += area_cmd
    if office != u'' and office != u'所有':
        off_cmd = 'Sheet_Form.ks_name == office'
        sel_cmd += off_cmd
    sel_cmd += ')).all()'
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