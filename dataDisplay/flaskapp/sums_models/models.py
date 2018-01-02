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

