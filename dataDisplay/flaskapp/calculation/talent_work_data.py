# -*- coding: utf-8 -*-
"""
# @Time    :2017/9/18 下午3:04
# @Author  :Xuxian
"""

from sqlalchemy import and_
import pandas
from dataDisplay.flaskapp.models import *


def cal():
    nums = []
    for year in range(2005, 2018):
        num = []
        result0 = result_15.query.filter(
            and_(result_15.cate.like('企业院士工作站'), result_15.re_time == str(year))).all()  # 省级院士工作站
        result1 = result_16.query.filter(
            and_(result_16.cate.like('苏州院士工作站'), result_16.re_year == str(year))).all()  # 苏州院士工作站
        result2 = result_37.query.filter(result_37.re_year == str(year)).all()  # 研究生工作站
        result3 = law_1.query.filter(
            and_(law_1.nation_kind.like('千人计划'), law_1.identify_year == str(year))).all()  # 千人计划
        result4 = law_1.query.filter(
            and_(law_1.nation_kind.like('万人计划'), law_1.identify_year == str(year))).all()  # 万人计划
        result5 = law_1.query.filter(
            and_(law_1.nation_kind.like('推进计划'), law_1.identify_year == str(year))).all()  # 推进计划

        # ----------------------------------------------------------------------------------
        result6 = law_1.query.filter(
            and_(law_1.province_team.like('省人才团队'), law_1.identify_year == str(year))).all()  # 省创新团队(全部)
        tmp = set()
        for i in range(len(result6)):
            tmp.add(result6[i].undertake_company)
        result6_num = len(tmp)

        result7 = law_1.query.filter(
            and_(law_1.province_team.like('省人才团队'), law_1.identify_year == str(year),
                 law_1.pro_name.like('%条线'))).all()  # 省创新团队(其他条线)
        result7_num = len(result7)
        result6_num = result6_num - result7_num     # 省创新团队(科技条线)
        # ----------------------------------------------------------------------------------
        result8 = law_1.query.filter(
            and_(law_1.province_kind.like('省人才'), law_1.identify_year == str(year))).all()  # 省双创人才(全部)

        result9 = law_1.query.filter(
            and_(law_1.province_kind.like('省人才'), law_1.identify_year == str(year),
                 law_1.pro_name.like('%条线'))).all()  # 省双创人才(其他条线)
        result8_num = len(result8) - len(result9)  # 省双创人才(科技条线)
        # ----------------------------------------------------------------------------------
        result10 = law_1.query.filter(
            and_(law_1.gusu_kind.like('姑苏人才'), law_1.identify_year == str(year))).all()  # 姑苏人才(all)
        result11 = law_1.query.filter(and_(law_1.gusu_kind.like('姑苏人才'), law_1.identify_year == str(year),
                                           law_1.pro_name.like('%条线'))).all()  # 姑苏人才(其他条线)
        result10_num = len(result10) - len(result11)  # 姑苏人才(科技)
        # ----------------------------------------------------------------------------------
        result12 = law_1.query.filter(
            and_(law_1.gusu_team.like('姑苏团队'), law_1.identify_year == str(year))).all()  # 姑苏团队
        tmp = set()
        for i in range(len(result12)):
            tmp.add(result12[i].undertake_company)
        result12_num = len(tmp)

        result13 = law_1.query.filter(
            and_(law_1.kunshan_team.like('昆山团队'), law_1.identify_year == str(year))).all()  # 昆山双创团队
        tmp = set()
        for i in range(len(result13)):
            tmp.add(result13[i].undertake_company)
        result13_num = len(tmp)

        result14 = law_1.query.filter(
            and_(law_1.kunshan_kind.like('昆山人才'), law_1.identify_year == str(year))).all()  # 昆山双创人才
        result15 = cop_ex_6.query.filter(cop_ex_6.sta_time == str(year)).all()  # 产学研联合项目
        result16 = cop_ex_7.query.filter(cop_ex_7.re_time == str(year)).all()  # 产学研联合体

        num.append(len(result0))
        num.append(len(result1))
        num.append(len(result2))
        num.append(len(result3))
        num.append(len(result4))
        num.append(len(result5))
        num.append(result6_num)
        num.append(len(result7))
        num.append(result8_num)
        num.append(len(result9))
        num.append(result10_num)
        num.append(len(result11))
        num.append(result12_num)
        num.append(result13_num)
        num.append(len(result14))
        num.append(len(result15))
        num.append(len(result16))
        nums.append(num)

    return nums
