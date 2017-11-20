# -*- coding: utf-8 -*-

import datetime
import time

# 爬虫起始名字
BOT_NAME = 'business_data_spider'

# Scrapy将寻找爬虫的模块列表
SPIDER_MODULES = ['business_data_spider.spiders', 'business_data_spider.spiders.incremental_spider']

# 模块在哪里使用genspider命令创建新的爬虫
NEWSPIDER_MODULE = 'business_data_spider.spiders'

# MongoDB数据库地址
MONGODB_HOST = '127.0.0.1'
# MongoDB数据库端口
MONGODB_PORT = 27017
# MongoDB数据库名称
MONGODB_NAME = 'business_data'
# 存放MD5的数据库名称
SECOND_MONGODB_NAME = "business_data_md5"
# 存放监控数据的数据库名称
SPY_SPIDER_MONGODB_NAME = "business_spy"

# 爬虫的一些公共变量设置
# 爬虫默认地址
URL = 'http://datagz.gov.cn/data/catalog/detail.do?method=QueryDataItem&'
# 默认起始页数
DEFAULT_BEGIN_PAGE_NUM = 1
# 每页数据最大的行数
MAX_ROWS_PER_PAGE = 10000

# 爬虫ID
# 商事主体经营异常名录信息
ABNORMAL_ID = 56299
# 广州市工商局行政处罚汇总信息 ID
ADMINISTRATIVE_PENALTIES_ID = 35351
# 商事主体基础信息
BASIC_INFO_ID = 56183
# 广州市商事主体荣誉信息
HONOR_ID = 52543
# 商事主体股东信息
SHAREHOLDER_INFO_ID = 52443
# 商事主体公司年报基本信息
YEAR_INFO_ID = 52776

# 自定义命令
COMMANDS_MODULE = 'business_data_spider.commands'

# 配置Scrapy最大并发请求量(默认貌似是16个)
# CONCURRENT_REQUESTS = 32

# 下载延迟(请求延迟)
DOWNLOAD_DELAY = 2

# 对任何单个域执行的并发请求的最大数量。
# CONCURRENT_REQUESTS_PER_DOMAIN = 16

# 对任何单个IP执行的并发请求的最大数量
# CONCURRENT_REQUESTS_PER_IP = 16

# Cookies的开关
COOKIES_ENABLED = False

# LOG配置(以后做成web框架监控再使用)
# LOG_ENABLED = True
# LOG_ENCODING = 'UTF-8'
# LOG_FILE = BOT_NAME + "/logs/scrapy-spider-" \
#            + str(int(time.mktime(datetime.datetime.now().timetuple())) * 1000) + ".log"
# LOG_FORMAT = '%(asctime)s [%(name)s] %(filename)s %(lineno)d %(levelname)s: %(message)s'
# LOG_LEVEL = "DEBUG"

# telnet控制台(默认开启)
# TELNETCONSOLE_ENABLED = False

# 开启或禁用下载中间件
# SPIDER_MIDDLEWARES = {
#    'business_data_spider.middlewares.BusinessDataSpiderSpiderMiddleware': 543,
# }

# 开启下载中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'business_data_spider.middlewares.RotateUserAgentMiddleware': 400,
}

# Enable or disable extensions
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# 配置实体类管道(item-pipelines)
ITEM_PIPELINES = {
   'business_data_spider.pipelines.BusinessDataSpiderPipeline': 300,
}

# Scrapy的限速功能, 开启和配置限速功能(默认关闭)
# 中文解释参考极客学院的wiki: http://wiki.jikexueyuan.com/project/scrapy/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
