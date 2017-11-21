# -*- coding: utf-8 -*-


# 内部库
import time
from collections import OrderedDict

# 第三方库
from pymongo import MongoClient
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class BusinessDataSpiderPipeline(object):
    def __init__(self):
        # 连接到MongoDB数据库
        _conn = MongoClient(host=settings['MONGODB_HOST'], port=settings['MONGODB_PORT'])

        # 创建MongoDB数据库名称(数据源)
        self.db = _conn[settings['MONGODB_NAME']]

        # MD5数据库
        self.md5_db = _conn[settings['SECOND_MONGODB_NAME']]

        # 监控数据库
        self.spy_db = _conn[settings['SPY_SPIDER_MONGODB_NAME']]

        # 年报数据去重
        self.year_report_set = set()

    # 管道加载item
    def process_item(self, item, spider):
        # 独立管道入口
        if spider.name == "business_basic_info":
            self.pipeline_core_method(item=item, spider_name=spider.name)

        elif spider.name == "business_information_year":
            if (item['NBND'] in self.year_report_set) and (item['UPDATE_TIME'] in self.year_report_set):
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.year_report_set.add(item['NBND'])
                self.year_report_set.add(item['UPDATE_TIME'])
                self.pipeline_core_method(item=item, spider_name=spider.name)

        elif spider.name == "business_shareholder_information":
            self.pipeline_core_method(item=item, spider_name=spider.name)

        elif spider.name == "business_administrative_penalties":
            self.pipeline_core_method(item=item, spider_name=spider.name)

        elif spider.name == "business_abnormal":
            self.pipeline_core_method(item=item, spider_name=spider.name)

        elif spider.name == "business_honor":
            self.pipeline_core_method(item=item, spider_name=spider.name)

        return item

    # 核心方法(因为每一种都是一样的只有一个变量不同而已.所以抽出来写好了)
    def pipeline_core_method(self, item, spider_name):
        """
        主要核心就是：(每个爬虫对应一个管道)
        1. 创建集合连接对象
        2. 判断item长度
        3. 将item中的不属于核心数据的数据取出
        4. 将item中的核心数据写入到数据库
        5. 维护爬虫监控(监控数据写入到数据库)
        :param item:
        :param spider_name:
        :return: 没有返回值
        """

        # 创建数据源数据库对象
        col_src = self.db[spider_name]

        # 爬虫ID
        spider_id = item.pop('spider_id')

        # item长度作为启动和关闭的判断点
        if len(item) > 1:
            # 析出不要的字段数据
            curr_page = item.pop('page_num')
            total_page = item.pop('total_page')
            total_record = item.pop('total_record')
            start_status = item.pop('start_status')

            # 增量爬虫御用字段
            md5_data = item.pop('data_md5')

            # 写入核心数据
            col_src.insert(item)

            # 写入监控数据
            self.spider_spy_log(spider_id=spider_id,
                                spider_name=spider_name,
                                current_page=curr_page,
                                total_page=total_page,
                                total_items_count=total_record,
                                is_first=start_status)

            # 特殊处理
            if spider_name != "business_administrative_penalties":
                """
                business_administrative_penalties这个爬虫返回的数据不太复合结构型数据.
                因为这个数据是属于类文档型的(没有唯一标识符),以一种纯记录的类型进行存储,
                所以这个爬虫的增量爬虫的实现意义不大,而且目前这个爬虫在网页上的记录暂时只
                有131条,所以做增量爬虫并不会对速度影响很大.
                """
                # 写入MD5数据
                self.incremental_spider_data(spider_name=spider_name,
                                             data_id=item['ZCH'],
                                             data_md5=md5_data)

    # 爬虫监控维护
    def spider_spy_log(self, spider_id, spider_name, is_first=False,
                       current_page="", total_page="", total_items_count="",):

        # 创建一个MongoDB集合对象
        col = self.spy_db["Spider_Spy"]
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

    # 增量爬虫需要的数据
    def incremental_spider_data(self, spider_name, data_id, data_md5):

        # 创建MD5数据源库对象
        col_md5 = self.md5_db[spider_name + "_md5"]

        # 创建一个有序字典
        md5_order_dict = OrderedDict()
        # 基本所有的表都有这个字段，注册号
        md5_order_dict['id'] = data_id
        # 数据的MD5值
        md5_order_dict['md5_value'] = data_md5

        try:
            # 写入
            col_md5.insert(md5_order_dict)
        except Exception as err:
            print(err)
