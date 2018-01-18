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

    def __init__(self):
        pass

    def every_keshi_data(self, itemid):
        """
        :param itemid: 在科室列表页中，为各个科室固定了的编号
        :return: 各个科室的统计结果
        """
        if itemid == 1:
            info = extract_data_1.query.filter_by(ks_name='合作交流科').all()
        if itemid == 2:
            info = extract_data_1.query.filter_by(ks_name='专利科').all()
        if itemid == 3:
            info = extract_data_1.query.filter_by(ks_name='农社科').all()
        if itemid == 4:
            info = extract_data_1.query.filter_by(ks_name='法规科').all()
        if itemid == 5:
            info = extract_data_1.query.filter_by(ks_name='高新科').all()
        if itemid == 6:
            info = extract_data_1.query.filter_by(ks_name='成果科').all()
        if itemid == 7:
            info = extract_data_1.query.filter(extract_data_1.ks_name.like('%')).all()
        return info


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


def money_lev_k(id):
    """
    :param id:选择科室所对应的编号
    :return: 横坐标为级别，纵坐标为经费总额，各个区镇在此情况下的走势
    """
    Data = extract_data_1()
    res, area_data = [], []
    ks_info = Data.every_keshi_data(id)
    for m in range(12):
        res.append([0,0,0,0])
        area_data.append([])
    for i in ks_info:
        if i.money == u'':
            continue
        elif i.area == u'市属':
            area_data[0].append(i)
        elif i.area == u'高新区':
            area_data[1].append(i)
        elif i.area == u'开发区':
            area_data[2].append(i)
        elif i.area == u'巴城':
            area_data[3].append(i)
        elif i.area == u'花桥':
            area_data[4].append(i)
        elif i.area == u'周市':
            area_data[5].append(i)
        elif i.area == u'千灯':
            area_data[6].append(i)
        elif i.area == u'张浦':
            area_data[7].append(i)
        elif i.area == u'周庄':
            area_data[8].append(i)
        elif i.area == u'淀山湖':
            area_data[9].append(i)
        elif i.area == u'陆家':
            area_data[10].append(i)
        elif i.area == u'锦溪':
            area_data[11].append(i)
    for j in range(12):
        for q in area_data[j]:
            if q.lev == u'国家':
                res[j][0] += float(i.money)
            elif q.lev == u'省级':
                res[j][1] += float(i.money)
            elif q.lev == u'苏州':
                res[j][2] += float(i.money)
            elif q.lev == u'昆山':
                res[j][3] += float(i.money)
    return res


def pronum_area_lev(id):
    """
    :param id:选择科室所对应的编号
    :return: 各区镇在各个级别下的项目总数
    """
    Data = extract_data_1()
    res, lev_data = [], []
    ks_info = Data.every_keshi_data(id)
    for m in range(4):
        res.append([0,0,0,0,0,0,0,0,0,0,0,0])
        lev_data.append([])
    for i in ks_info:
        if i.lev == u'':
            continue
        elif i.lev == u'国家':
            lev_data[0].append(i)
        elif i.lev == u'省级':
            lev_data[1].append(i)
        elif i.lev == u'苏州':
            lev_data[2].append(i)
        elif i.lev == u'昆山':
            lev_data[3].append(i)
    for j in range(4):
        for q in lev_data[j]:
            if q.area == u'':
                continue
            elif q.area == u'市属':
                res[j][0] += 1
            elif q.area == u'高新区':
                res[j][1] += 1
            elif q.area == u'开发区':
                res[j][2] += 1
            elif q.area == u'巴城':
                res[j][3] +=1
            elif q.area == u'花桥':
                res[j][4] += 1
            elif q.area == u'周市':
                res[j][5] += 1
            elif q.area == u'千灯':
                res[j][6] += 1
            elif q.area == u'张浦':
                res[j][7] += 1
            elif q.area == u'周庄':
                res[j][8] += 1
            elif q.area == u'淀山湖':
                res[j][9] += 1
            elif q.area == u'陆家':
                res[j][10] += 1
            elif q.area == u'锦溪':
                res[j][11] += 1
    return res


def money_area_year_lev(id):
    """
    :param id: 选择科室对应的编号
    :return: 各区镇在相应年份内内各级别下项目经费总额
    """
    Data = extract_data_1()
    res,  area_year_data = [], []
    ks_info = Data.every_keshi_data(id)
    area_num, year_num = 12, 13
    for i in range(area_num):
        area_data, res_tmp, area_year_temp = [], [], []
        for j in range(year_num):
            area_data.append([])
            res_tmp.append([])
            area_year_temp.append([])
        area_year_data.append(area_year_temp)
        res.append(res_tmp)


    for i in ks_info:
        i.year = i.year.replace(u',', u'')
        if len(i.year) == 8:
            i.year = i.year[:4]

    # 按区镇将数据分类
    for i in ks_info:
        if i.money == u'':
            continue
        elif i.area == u'市属':
            area_data[0].append(i)
        elif i.area == u'高新区':
            area_data[1].append(i)
        elif i.area == u'开发区':
            area_data[2].append(i)
        elif i.area == u'巴城':
            area_data[3].append(i)
        elif i.area == u'花桥':
            area_data[4].append(i)
        elif i.area == u'周市':
            area_data[5].append(i)
        elif i.area == u'千灯':
            area_data[6].append(i)
        elif i.area == u'张浦':
            area_data[7].append(i)
        elif i.area == u'周庄':
            area_data[8].append(i)
        elif i.area == u'淀山湖':
            area_data[9].append(i)
        elif i.area == u'陆家':
            area_data[10].append(i)
        elif i.area == u'锦溪':
            area_data[11].append(i)

    # 在各类区镇数据中，按年份分类
    for i in range(13):
        for q in area_data[i]:
            try:
                if q.year == u'':
                    continue
                elif int(q.year) <= 2005:
                    area_year_data[i][0].append(q)
                else:
                    area_year_data[i][int(q.year) - 2005].append(q)
            except:
                pass

            # elif int(q.year) == 2006:
            #     area_year_data[i][1].append(q)
            # elif int(q.year) == 2007:
            #     area_year_data[i][2].append(q)
            # elif int(q.year) == 2008:
            #     area_year_data[i][3].append(q)
            # elif int(q.year) == 2009:
            #     area_year_data[i][4].append(q)
            # elif int(q.year) == 2010:
            #     area_year_data[i][5].append(q)
            # elif int(q.year) == 2011:
            #     area_year_data[i][6].append(q)
            # elif int(q.year) == 2012:
            #     area_year_data[i][7].append(q)
            # elif int(q.year) == 2013:
            #     area_year_data[i][8].append(q)
            # elif int(q.year) == 2014:
            #     area_year_data[i][9].append(q)
            # elif int(q.year) == 2015:
            #     area_year_data[i][10].append(q)
            # elif int(q.year) == 2016:
            #     area_year_data[i][11].append(q)



    # 这里统计各个区镇下，各个年份下的四个级别的经费总额
    for i in range(12):
        for j in range(13):
            for k in range(4):
                res[i][j].append(0)
            for p in area_year_data[i][j]:
                if p:

                    if p.lev == u'':
                        continue
                    elif p.lev == u'国家':
                        res[i][j][0] += float(p.money)
                    elif p.lev == u'省级':
                        res[i][j][1] += float(p.money)
                    elif p.lev == u'苏州':
                        res[i][j][2] += float(p.money)
                    elif p.lev == u'昆山':
                        res[i][j][3] += float(p.money)
    return res