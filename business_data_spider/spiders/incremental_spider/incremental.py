# -*- coding: UTF-8 -*-
"""
Created on 2017年11月10日
@author: Leo
"""

# 系统库
import json
import logging
import urllib.parse as up
from collections import OrderedDict

# 第三方库
import scrapy
from scrapy.conf import settings
from pymongo import MongoClient

# 项目内部库
from business_data_spider.utils.util import data_transfer_md5


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger()


# 增量爬虫
class Incremental(scrapy.Spider):
    name = "spider_incremental"

    def __init__(self, **kwargs):
        # 爬虫ID和名称对应的字典
        self.cata_id_pool = [{"business_abnormal": settings['ABNORMAL_ID'],
                              "business_basic_info": settings['BASIC_INFO_ID'],
                              "business_honor": settings['HONOR_ID'],
                              "business_shareholder_information": settings['SHAREHOLDER_INFO_ID'],
                              "business_information_year": settings['YEAR_INFO_ID']}]

        # 地址池
        self.url_pool = \
            [settings['URL'] +
             up.urlencode(
                 {"cata_id": str(cata_id), "rows": str(10), "page": settings['DEFAULT_BEGIN_PAGE_NUM']}
             ) for spider_dict in self.cata_id_pool for (spider_name, cata_id) in spider_dict.items()]

        # 起始地址
        self.start_urls = [self.url_pool[0]]

        # 数据库链接
        self.db = MongoClient(host=settings['MONGODB_HOST'],
                              port=settings['MONGODB_PORT'])[settings['MONGODB_NAME']]

        self.md5_db = MongoClient(host=settings['MONGODB_HOST'],
                                  port=settings['MONGODB_PORT'])[settings['SECOND_MONGODB_NAME']]

        # 计数器变量
        self.spider_id = 0

        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], method="POST", callback=self.parse)

    def parse(self, response):
        # 截取当前url的cata_id
        cur_spider_id = [x for x in response.url.split("&") if 'cata_id' in x][0].split("=")[1]
        cur_spider_name = self.get_current_spider_info(cur_spider_id)

        if cur_spider_name == "business_abnormal" or cur_spider_name == "business_information_year":
            return

        # 数据库连接(原始数据源和MD5数据源)
        col = self.db[cur_spider_name]
        md5_col = self.md5_db[cur_spider_name + "_md5"]

        # 获取数据
        results = json.loads(bytes.decode(response.body), object_pairs_hook=OrderedDict)

        # 判断是否数据为空
        if len(results['rows']) == 0:
            scrapy.Spider.close(results, reason="All data has been collected.")

        # 解析数据
        for spider_result in results['rows']:
            data_md5 = data_transfer_md5(data=spider_result)

            # 判断是否出现过
            if col.find({"md5_value": data_md5}).count() == 0:
                logger.info("新增数据: " + str(spider_result))
                try:
                    # 更新原始数据和MD5数据
                    col.update({"ZCH": spider_result['ZCH']}, spider_result)
                    md5_col.update({"id", spider_result['ZCH']}, {"id": spider_result['ZCH'], "value": data_md5})
                except Exception as err:
                    logger.debug(err)

        # 下一个爬虫
        for url in enumerate(self.url_pool[1:]):
            yield scrapy.Request(url=url[1], method="POST", callback=self.parse)

    def get_current_spider_info(self, spider_id):
        return [spider_name
                for spider_dict in self.cata_id_pool
                for (spider_name, cata_id) in spider_dict.items()
                if cata_id == int(spider_id)][0]
