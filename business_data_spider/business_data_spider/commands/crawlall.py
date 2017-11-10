# -*- coding: utf-8 -*-
"""
Created on 2017年11月10日
@author: Leo
"""
from scrapy.commands import ScrapyCommand
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


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
        # process.crawl(one)
        # process.crawl(two)
        # process.start()