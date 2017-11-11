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

# 第三方库
import scrapy


# 广州市工商局行政处罚汇总信息，ID=35351
class BusinessAdministrativePenaltyInfo(scrapy.Spider):
    name = "business_administrative_penalties"

    def __init__(self, **kwargs):
        # 起始地址
        self.start_urls = ['http://datagz.gov.cn/data/catalog/detail.do?method=QueryDataItem&']

        # 爬虫ID
        self._category_id = 35351

        # 每一页的数量
        self._page_max_rows = 10000

        # 请求页面拼接的数据
        self.post_data = {
            "cata_id": str(self._category_id),  # 目录号
            "rows": str(self._page_max_rows),  # 每页的数据量
            "page": 1,  # 页码
        }

        # super方法
        super().__init__(**kwargs)

    def start_requests(self):
        # 请求链接
        post_url = self.start_urls[0] + up.urlencode(self.post_data)
        yield scrapy.Request(url=post_url, method="POST", callback=self.parse)

    def parse(self, response):
        # 获取数据
        penalties_info = json.loads(bytes.decode(response.body))
        for penalty in penalties_info['rows']:
            # 添加数据年份和最近更新的时间戳
            penalty.update(dict(statistics_year=datetime.datetime.now().year))
            penalty.update(dict(last_update_time=int(time.mktime(datetime.datetime.now().timetuple())) * 1000))
            data_item = penalty
            yield data_item

        # 最大上限页数
        max_page = penalties_info['total']
        if self.post_data['page'] + 1 <= max_page:
            self.post_data['page'] += 1
            post_url = self.start_urls[0] + up.urlencode(self.post_data)
            yield scrapy.Request(url=post_url, method="POST", callback=self.parse)

