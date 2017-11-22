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
    for index in range(len(data)):
        # 将缺省值做null处理
        if str(data[index]).strip():
            value = data[index]
        else:
            value = None
        setattr(self, columns[index], value)


class sums_8(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    year = db.Column(db.TEXT)
    ac_workstation_gov = db.Column(db.TEXT)
    ac_workstation_sz = db.Column(db.TEXT)
    master_ws = db.Column(db.TEXT)
    qianren_all = db.Column(db.TEXT)
    qianren_coustom = db.Column(db.TEXT)
    wanren = db.Column(db.TEXT)
    tec_plan = db.Column(db.TEXT)
    gov_in_team_tec = db.Column(db.TEXT)
    gov_in_team_all = db.Column(db.TEXT)
    gov_in_team_other = db.Column(db.TEXT)
    gov_in_person_tec = db.Column(db.TEXT)
    gov_in_person = db.Column(db.TEXT)
    gs_person_tec = db.Column(db.TEXT)
    gs_person_other = db.Column(db.TEXT)
    gs_team = db.Column(db.TEXT)
    ks_team = db.Column(db.TEXT)
    ks_person = db.Column(db.TEXT)
    union_project = db.Column(db.TEXT)
    union_base = db.Column(db.TEXT)
    rate_con_person = db.Column(db.TEXT)
    sum_person = db.Column(db.TEXT)
    person_research = db.Column(db.TEXT)
    rate_con_tec = db.Column(db.TEXT)
    rate_sta_civ = db.Column(db.TEXT)

    def __repr__(self):
        return 'info:{}'.format(self.id)

    def __init__(self, columns, data):
        init_databse(self, columns, data)


class sums_3(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    year = db.Column(db.TEXT)
    torch_com = db.Column(db.TEXT)
    creation_com = db.Column(db.TEXT)
    gxjs_identity = db.Column(db.TEXT)
    gxjs_effictive = db.Column(db.TEXT)
    advance_com = db.Column(db.TEXT)
    gov_creation_com = db.Column(db.TEXT)
    folk_com = db.Column(db.TEXT)
    tech_mic_com = db.Column(db.TEXT)
    con_imp_product = db.Column(db.TEXT)
    con_creation_product = db.Column(db.TEXT)
    gov_eff_product = db.Column(db.TEXT)
    gov_creation_product = db.Column(db.TEXT)
    gov_imp_product = db.Column(db.TEXT)
    sz_eff_product = db.Column(db.TEXT)
    soft_com = db.Column(db.TEXT)
    soft_product = db.Column(db.TEXT)

    def __repr__(self):
        return 'info:{}'.format(self.id)

    def __init__(self, columns, data):
        init_databse(self, columns, data)
