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

# 第三方库
import scrapy
from scrapy.conf import settings
from pymongo import MongoClient


# 商事主体经营异常名录信息，ID=56299 Total=879360
class BusinessAbnormal(scrapy.Spider):
    name = "business_abnormal"

    # 爬虫ID
    spider_id = uuid.uuid1()

    # 初次启动的变量
    first_start = True

    def __init__(self, **kwargs):
        # 起始地址
        self.start_urls = ['http://datagz.gov.cn/data/catalog/detail.do?method=QueryDataItem&']

        # 请求页面拼接的数据
        self.post_data = {
            "cata_id": str(settings['ABNORMAL_ID']),  # 目录号
            "rows": str(settings['MAX_ROWS_PER_PAGE']),  # 每页的数据量
            "page": settings['DEFAULT_BEGIN_PAGE_NUM'],  # 页码
        }

        # super方法
        super().__init__(**kwargs)

    def start_requests(self):
        # 请求链接
        post_url = self.start_urls[0] + up.urlencode(self.post_data)
        yield scrapy.Request(url=post_url, method="POST", callback=self.parse)

    def parse(self, response):
        # 获取数据
        abnormal_business = json.loads(bytes.decode(response.body))

        # 判断是否数据为空
        if len(abnormal_business['rows']) == 0:
            scrapy.Spider.close(BusinessAbnormal, reason="All data has been collected.")

        # 解析数据
        for business in abnormal_business['rows']:
            # 添加数据年份和最近更新的时间戳
            business.update(dict(statistics_year=datetime.datetime.now().year))
            business.update(dict(last_update_time=int(time.mktime(datetime.datetime.now().timetuple())) * 1000))

            # 爬虫监控需要的数据(爬虫UUID,爬虫当前页面,爬虫总页数,爬虫总记录数)
            business.update(dict(spider_id=BusinessAbnormal.spider_id))
            business.update(dict(page_num=self.post_data['page']))
            business.update(dict(total_page=abnormal_business['total']))
            business.update(dict(total_record=abnormal_business['records']))
            business.update(dict(start_status=BusinessAbnormal.first_start))

            # 赋值给item
            data_item = business

            # 修改启动状态
            BusinessAbnormal.first_start = False

            yield data_item

        # 最大上限页数
        max_page = abnormal_business['total']
        if self.post_data['page'] + 1 <= max_page:
            self.post_data['page'] += 1
            post_url = self.start_urls[0] + up.urlencode(self.post_data)
            yield scrapy.Request(url=post_url, method="POST", callback=self.parse)
        else:
            # 关闭时的操作(很无奈,找不到啥解决办法再parse方法里加入结束的判断)
            col = MongoClient(host=settings['MONGODB_HOST'],
                              port=settings['MONGODB_PORT'])[settings['MONGODB_NAME']]['Spider_Spy']
            close_item = dict(spider_endTime=int(round(time.time() * 1000)),
                              spider_status="ClosedOrFinished")
            col.update({"spider_id": BusinessAbnormal.spider_id}, {'$set': close_item}, upsert=True)

            scrapy.Spider.close(BusinessAbnormal, reason="All data has been collected.")
