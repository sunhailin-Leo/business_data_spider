# -*- coding: UTF-8 -*-
"""
Created on 2017年11月10日
@author: Leo
"""

import hashlib


# 将json数据转成字符串格式后进行
def data_transfer_md5(data):
    md5_str = hashlib.md5(str(data).encode("gb2312")).hexdigest()
    return md5_str
