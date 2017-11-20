# -*- coding: UTF-8 -*-
"""
Created on 2017年11月20日
@author: Leo
"""

# 系统内部库
import sys
import time

# 第三方库
import schedule
from scrapy import cmdline


class TimeTask:
    def __init__(self, args_list):
        self._options = args_list[::2]
        self._variable = args_list[1::2]

    def validate_option(self):
        # 判断是否有参数
        if self._options is None or self._options is "" or len(self._options) == 0:
            self.help_center()
            raise ValueError("No argument!")

        else:
            # 判断有参数的情况
            if "-h" or "--help" or "--h" in self._options:
                self.help_center()


    def help_center(self):
        print("usage: python [option] ... [-t time string] [-m model name]")
        print("Options and arguments (and corresponding environment variables):")
        print("-s\t:You give me a seconds number arguments like 10(every 10 secs)")
        print("-m\t:You give me a minutes number arguments like 2(every 2 minutes)")
        print("-h\t:You give me a hours number arguments like 2(every 2 hours)")
        print("-d\t:You give me a days number arguments like 3(every 3 days)")
        print("-w\t:You give me a weekdays number arguments like 3(every Wednesday), 0 is Sunday")
        print("-t\t:You give me a time arguments like 18:00 (every day at 18:00 will start this job)")
        print("-j\t:What job do you want to do? like execute('scrapy crawl spider_incremental')")

    def create_job(self):
        schedule.every(5).seconds.do(self.job1)
        # schedule.every().monday.do(self.job1)
        # schedule.every().minute.do()
        # schedule.every().hour.do()
        # schedule.every().day().do()
        # schedule.every().weeks(1).do()
        # schedule.every().monday.do()

    def job1(self):
        print("Job1")
        # time.sleep(3)

    def start_job(self):
        # 校验参数
        self.validate_option()

        # 发布定时任务
        self.create_job()

        # 启动
        while True:
            schedule.run_pending()


if __name__ == '__main__':
    args = sys.argv[1:]
    T = TimeTask(args_list=args)
    T.start_job()