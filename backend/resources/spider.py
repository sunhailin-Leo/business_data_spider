# -*- coding: UTF-8 -*-
"""
Created on 2017年11月10日
@author: Leo
"""

from bson import UUIDLegacy
from bson.binary import UUID
# 第三方库
from flask import jsonify
from flask_restful import Resource, reqparse

from backend.common.validate import DataValidate
# 系统内部库
from backend.common.mgo import MgoConf


# 获取爬虫的状态列表
class SpiderList(Resource):
    def __init__(self):
        # 数据库连接对象
        self.mgo = MgoConf()

        # 数据校验方法
        self.v = DataValidate()

        # get方法的parser
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('sid', location=['args'])
        self.get_parser.add_argument('pn', location=['args'], type=int)
        self.get_parser.add_argument('r', location=['args'], type=int)

    def get(self):
        # 获取参数列表并解析
        args = self.get_parser.parse_args()
        spider_id = args['sid']
        page_num = args['pn']
        rows = args['r']

        # 判断spider_id是否为空,空则查全部,非空则按编号查询.但是页码不能为空,默认返回20条
        if spider_id == "" and page_num >= 0 and rows >= 0:
            data = self.mgo.find_data(db_name="Spider_Spy",
                                      page_num=page_num - 1,
                                      limit=rows)
            return jsonify(data)

        # 判断spider_id不为空,
        elif spider_id != "" and page_num >= 0 and rows >= 0:
            data = self.mgo.find_data(db_name="Spider_Spy",
                                      query={"spider_id": UUIDLegacy(UUID(spider_id))},
                                      page_num=page_num - 1,
                                      limit=rows)
            return jsonify(data)

        return jsonify({"msg": "Not Result!Parameter is invalid!"})


# 搜索功能, 条件查询(前端搜索)
class SpiderSearch(Resource):
    def __init__(self):
        # 数据库连接对象
        self.mgo = MgoConf()

        # get方法的parser
        self.get_parser = reqparse.RequestParser()
        self.get_parser.add_argument('name', location=['args'], type=str)

    def get(self):
        # 获取参数列表并解析
        args = self.get_parser.parse_args()
        name = args['name']
        # page_num = args['pn']
        # rows = args['r']

        # 查询
        if name != "":
            data = self.mgo.find_data(db_name="Spider_Spy",
                                      query={"spider_name": name}, page_num=0)
            return jsonify(data)

        else:
            data = self.mgo.find_data(db_name="Spider_Spy", page_num=0)
            return jsonify(data)


# 发布定时任务
class ScheduleSpiderTaskProvider(Resource):
    def __init__(self):
        pass

    def post(self):
        pass
