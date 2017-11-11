# -*- coding: utf-8 -*-
"""
Created on 2017年11月10日
@author: Leo
"""
from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess

from business_data_spider.spiders import abnormal_business
from business_data_spider.spiders import administrative_penalty
from business_data_spider.spiders import basic_information
from business_data_spider.spiders import honor_business
from business_data_spider.spiders import shareholder_info
from business_data_spider.spiders import year_report


class Command(ScrapyCommand):
    requires_project = True

    def syntax(self):
        return '[options]'

    def short_desc(self):
        return 'Runs all of the spiders'

    def add_options(self, parser):
        ScrapyCommand.add_options(self, parser)

    def process_options(self, args, opts):
        ScrapyCommand.process_options(self, args, opts)

    def run(self, args, opts):
        settings = get_project_settings()
        # 爬虫类
        process = CrawlerProcess(settings)
        # 多爬虫
        process.crawl(abnormal_business.BusinessAbnormal)
        process.crawl(administrative_penalty.BusinessAdministrativePenaltyInfo)
        process.crawl(basic_information.BasicInformation)
        process.crawl(honor_business.BusinessHonor)
        process.crawl(shareholder_info.BusinessShareHolderInfo)
        process.crawl(year_report.BusinessYearReport)
        # 启动
        process.start()