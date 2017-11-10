# -*- coding: utf-8 -*-

from pymongo import MongoClient
from scrapy.conf import settings


class BusinessDataSpiderPipeline(object):
    def __init__(self):
        # 连接到数据库
        _conn = MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])

        # 创建数据库名称
        self.db = _conn[settings['MONGODB_NAME']]

    def process_item(self, item, spider):
        if spider.name == "business_basic_info":
            col = self.db[spider.name]
            col.insert(item)
        elif spider.name == "business_information_year":
            col = self.db[spider.name]
            col.insert(item)
        elif spider.name == "business_shareholder_information":
            col = self.db[spider.name]
            col.insert(item)
        elif spider.name == "business_administrative_penalties":
            col = self.db[spider.name]
            col.insert(item)
        elif spider.name == "business_abnormal":
            col = self.db[spider.name]
            col.insert(item)
        elif spider.name == "business_honor":
            col = self.db[spider.name]
            col.insert(item)
        return item
