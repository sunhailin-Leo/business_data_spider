# -*- coding: utf-8 -*-


# 内部库
import datetime
import time

from collections import OrderedDict

# 第三方库
from pymongo import MongoClient
from scrapy.conf import settings


class BusinessDataSpiderPipeline(object):
    def __init__(self):
        # 连接到数据库
        _conn = MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])

        # 创建数据库名称
        self.db = _conn[settings['MONGODB_NAME']]

    # 管道加载item
    def process_item(self, item, spider):
        """
        重复代码的主要核心就是：
        1. 创建集合连接对象
        2. 判断item长度
        3. 将item中的不属于核心数据的数据取出
        4. 将item中的核心数据写入到数据库
        5. 维护爬虫监控(监控数据写入到数据库)

        :param item:
        :param spider:
        :return:

        """
        if spider.name == "business_basic_info":
            col = self.db[spider.name]
            spider_id = item.pop('spider_id')
            col.insert(item)

        elif spider.name == "business_information_year":
            col = self.db[spider.name]
            spider_id = item.pop('spider_id')
            col.insert(item)

        elif spider.name == "business_shareholder_information":
            col = self.db[spider.name]
            spider_id = item.pop('spider_id')
            col.insert(item)

        elif spider.name == "business_administrative_penalties":
            # 创建数据库对象
            col = self.db[spider.name]

            # 爬虫ID
            spider_id = item.pop('spider_id')

            # item长度作为启动和关闭的判断点
            if len(item) > 1:
                # 析出不要的字段数据
                curr_page = item.pop('page_num')
                total_page = item.pop('total_page')
                total_record = item.pop('total_record')
                start_status = item.pop('start_status')

                # 写入核心数据
                col.insert(item)

                # 写入监控数据
                self.spider_spy_log(spider_id=spider_id,
                                    spider_name=spider.name,
                                    current_page=curr_page,
                                    total_page=total_page,
                                    total_items_count=total_record,
                                    is_first=start_status)

        elif spider.name == "business_abnormal":
            col = self.db[spider.name]
            spider_id = item.pop('spider_id')
            col.insert(item)

        elif spider.name == "business_honor":
            col = self.db[spider.name]
            spider_id = item.pop('spider_id')
            col.insert(item)

        return item

    # 爬虫监控维护
    def spider_spy_log(self, spider_id, spider_name, is_first=False,
                       current_page="", total_page="", total_items_count="",):

        # 创建一个MongoDB集合对象
        col = self.db["Spider_Spy"]
        # 创建唯一索引
        col.ensure_index('spider_id', unique=True)

        # 有序字典
        spy_order = OrderedDict()

        if is_first:
            # 爬虫uuid
            spy_order['spider_id'] = spider_id
            # 启动时间
            spy_order['spider_createTime'] = int(round(time.time() * 1000))
            # 爬虫名称
            spy_order['spider_name'] = spider_name
            # 爬虫结束时间
            spy_order['spider_endTime'] = ""

        # 爬虫状态
        spy_order['spider_status'] = "Running"
        # 爬虫正在爬取的页码
        spy_order['spider_currPage'] = current_page
        # 爬虫需要爬去的总页数
        spy_order['total_page'] = total_page
        # 爬虫需要爬取的总条数
        spy_order['spider_all_items'] = total_items_count

        try:
            # 写入数据库(需要使用MongoDB中的upsert功能)
            col.update({"spider_id": spider_id}, {'$set': spy_order}, upsert=True)
        except Exception as err:
            print(err)