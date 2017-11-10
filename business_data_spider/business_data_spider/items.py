# -*- coding: utf-8 -*-

import scrapy


# 商事主体基础信息 ID=56183
class BusinessBasicInformationItem(scrapy.Item):
    basic_info = {}

    def __setitem__(self, key, value):
        self.basic_info[key] = value


# 商事主体公司年报基本信息 ID=52776
class BusinessInformationYearItem(scrapy.Item):
    year_info = {}

    def __setitem__(self, key, value):
        self.year_info[key] = value


# 商事主体股东信息，ID=52443
class BusinessShareholderInformationItem(scrapy.Item):
    shareholder_Info = {}

    def __setitem__(self, key, value):
        self.shareholder_Info[key] = value


# 广州市工商局行政处罚汇总信息，ID=35351
class BusinessAdministrativePenaltiesItem(scrapy.Item):
    penalties_info = {}

    def __setitem__(self, key, value):
        self.penalties_info[key] = value


# 商事主体经营异常名录信息，ID=56299
class BusinessAbnormalItem(scrapy.Item):
    abnormal_info = {}

    def __setitem__(self, key, value):
        self.abnormal_info[key] = value


# 广州市商事主体荣誉信息，ID=52543
class BusinessHonorItem(scrapy.Item):
    honor_info = {}

    def __setitem__(self, key, value):
        self.honor_info[key] = value
