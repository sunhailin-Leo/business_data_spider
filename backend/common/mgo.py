# -*- coding: UTF-8 -*-
"""
Created on 2017年11月10日
@author: Leo
"""

# 第三方库
from pymongo import MongoClient


class MgoConf:
    def __init__(self):
        _conn = MongoClient(host="127.0.0.1", port=27017)
        self.db = _conn['business_spy']

    # CRUD操作

    # 插入
    def insert_data(self, data, db_name):
        """
        data要字典类型的,就是json数据
        db_name就是集合名collection
        :param data:
        :param db_name:
        :return: json结果
        """
        # 创建集合对象
        col = self.db[db_name]
        try:
            col.insert(data)
            return {'msg': 'Success', 'status': True}
        except Exception as err:
            return {'msg': str(err), 'status': False}

    # 查找数据
    def find_data(self, db_name, page_num, query=None, limit=20):
        """
        :param db_name: collection名
        :param query: 查询条件语句 mongo语法
        :param limit: 分页查询的参数，一页限制多少，默认20个
        :param page_num: 分页查询的参数，页码, 默认1
        :return: 返回数据成功与否和查询到的数据
        """
        # 如果query条件参数
        if query is None:
            query = {}

        # 限制查询个数
        if limit >= 100:
            return {'msg': "Can not select to much data!", 'status': False, 'data': None}

        # 偏移量
        pos = page_num * limit

        # 创建集合对象
        col = self.db.get_collection(name=db_name)

        try:
            # 如果query为{}默认就是分页查全部。（条件查询）
            result = [x for x in col.find(query, {"_id": 0}).limit(limit).skip(pos)]
            result_count = col.find().count()
            return {'msg': 'Success', 'status': True, 'data': result, 'count': result_count}
        except Exception as err:
            return {'msg': str(err), 'status': False, 'data': None}

    # 更新数据
    def update_data(self):
        pass

    # 删除数据
    def delete_data(self):
        pass
