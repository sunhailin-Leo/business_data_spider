# -*- coding: UTF-8 -*-
"""
Created on 2017年11月10日
@author: Leo
"""


class DataValidate:

    # 校验是否为数字
    @staticmethod
    def is_int(data):
        if isinstance(data, int):
            return {"status": True, "data": data}
        else:
            return {"status": False, "data": data}

    # 校验是否为字符串
    @staticmethod
    def is_str(data):
        if isinstance(data, str):
            return {"status": True, "data": data}
        else:
            return {"status": False, "data": data}