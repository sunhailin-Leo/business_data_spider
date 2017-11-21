# -*- coding: UTF-8 -*-
"""
Created on 2017年11月20日
@author: Leo
"""

# 系统内部库
import sys
import inspect
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
            # 判断参数长度
            if len(self._options) > 2:
                raise ValueError("Arguments is out of range!")
            else:
                # 判断有参数的情况
                if ("-h" in self._options) or ("--help" in self._options):
                    self.help_center()
                    return True
                else:
                    if "-j" not in self._options:
                        raise ValueError("No job to run!")
                    else:
                        option_dict = {}
                        for key, value in enumerate(self._options):
                            option_dict[value] = self._variable[key]
                        print(option_dict)

    @staticmethod
    def help_center():
        print("usage: python [option] ... [-t time string] [-m model name]")
        print("Options and arguments (and corresponding environment variables):")
        print("-s\t:You give me a seconds number arguments like 10(every 10 secs)")
        print("-m\t:You give me a minutes number arguments like 2(every 2 minutes)")
        print("-hour\t:You give me a hours number arguments like 2(every 2 hours)")
        print("-d\t:You give me a days number arguments like 3(every 3 days)")
        print("-w\t:You give me a weekdays number arguments like 3(every Wednesday), 0 is Sunday")
        print("-t\t:You give me a time arguments like 18:00 (every day at 18:00 will start this job)")
        print("-j\t:What job do you want to do? like execute('scrapy crawl spider_incremental')")
        print("-h, --help or --h\t:We give you a help to explain the arguments.")

    def create_job(self):
        schedule.every(5).seconds.do(self.job1)
        # schedule.every().minute.do(self.job1)
        # schedule.every().hour.do(self.job1)
        # schedule.every().day().do()
        # schedule.every().weeks(1).do()
        # schedule.every().monday.do()

    @staticmethod
    def get_current_function_name():
        for i in inspect.stack():
            print(i)
        # print(sys._getframe().f_code.co_name)

    def job1(self):
        print("Job1")
        # time.sleep(3)

    def start_job(self):
        # 校验参数
        # self.validate_option()

        self.get_current_function_name()

        # # 发布定时任务
        # self.create_job()
        #
        # # 启动
        # while True:
        #     schedule.run_pending()


if __name__ == '__main__':
    args = sys.argv[1:]
    T = TimeTask(args_list=args)
    T.start_job()