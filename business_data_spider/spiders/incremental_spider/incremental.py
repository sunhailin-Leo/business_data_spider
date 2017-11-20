# -*- coding: UTF-8 -*-
"""
Created on 2017年11月10日
@author: Leo
"""

# 系统库
import datetime
import json
import time
import urllib.parse as up
import uuid
from collections import OrderedDict

# 第三方库
import scrapy
from scrapy.conf import settings
from pymongo import MongoClient

# 项目内部库
from business_data_spider.utils.util import data_transfer_md5


# 增量爬虫
class Incremental(scrapy.Spider):
    name = "incremental_spider"

    def __init__(self, **kwargs):
        # ID池
        self.cata_id_pool = [settings['ABNORMAL_ID'],
                             settings['ADMINISTRATIVE_PENALTIES_ID'],
                             settings['BASIC_INFO_ID'],
                             settings['HONOR_ID'],
                             settings['SHAREHOLDER_INFO_ID'],
                             settings['YEAR_INFO_ID']]

        # 拼接URL的参数
        self.post_data = {
            "cata_id": str(settings['ABNORMAL_ID']),  # 目录号
            "rows": str(5),  # 每页的数据量
            "page": settings['DEFAULT_BEGIN_PAGE_NUM'],  # 页码
        }

        # 地址池
        self.url_pool = \
            [settings['URL'] +
             up.urlencode(
                 {"cata_id": str(cata_id), "rows": str(1000), "page": settings['DEFAULT_BEGIN_PAGE_NUM']}
             ) for cata_id in self.cata_id_pool]

        # 起始地址
        self.start_urls = [self.url_pool[0]]

        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], method="POST", callback=self.parse)

    def parse(self, response):
        # 获取数据
        result = json.loads(bytes.decode(response.body), object_pairs_hook=OrderedDict)
        print(result)

        for url in enumerate(self.url_pool[1:]):
            yield scrapy.Request(url=url[1], method="POST", callback=self.parse)