# 政务数据爬虫

---

<h4 id="Contract">开头唠叨两句</h4>

在使用中有任何问题，可以反馈给我，以下联系方式跟我交流

* Author: Leo
* Wechat: Leo-sunhailin
* QQ: 379978424
* E-mail: 379978424@qq.com
* Github URL: [Github传送门](https://github.com/sunhailin-Leo/business_data_spider)

---

* 开发环境
    * 系统版本： Win10 x64
    * Python版本: Python 3.4.4

---

* 安装方式

```Python
# 在项目根目录运行安装
pip install -r requirements.txt
```

---

* 运行方式

* 在根目录下的business_data_spider文件夹中(即和scarpy.cfg在同一路径下)
* Windows下按住shift + 右键打开命令行, Linux 就cd 到那个路径下
* 全量爬虫

```Python
scrapy crawlall

# 如果说有报错是 No module named 'win32api'的话,请执行如下命令:
pip install pypiwin32

```

* 单个爬虫

```Python
# 可以先使用以下命令查看当前有哪些爬虫
scrapy list

# 然后选择一个执行
scrapy crawl <你选择的爬虫名称>

```

---

<h3 id="issue">技术点、功能及一些注意事项</h3>

```Python

技术点:
    Scrapy(利用了CrawlProcess的线程模型进行多线程爬虫开发)
    MongoDB(监控模块Spider_Spy表设置了索引)

功能:
    1. 异步多线程获取所需要的政务数据(公司主体信息等等)
    2. 设计了监控模块(爬虫监控状态)
    3. 设置了LOG的输出到文件(但是不能同时输出到控制台和文件)

注意事项:
    1. 所有关于时间戳的统统精确到毫秒级
       (秒级的话如果只有一页的时候,监控那张表的开始和结束时间会显示在同一秒内完)
    2. 目前监控模块只在administrative_penalty.py中实现

```

<h3 id="future">未来开发的计划</h3>

```Python
1. 将监控模块全覆盖
2. 设计个通用爬虫,针对于本项目网站的政务数据
3. 研究下Scrapy的日志系统,看看是否能够拆分每一个爬虫对应每一个日志
4. 设计利用flask-restful + vue-admin做一个爬虫监控平台
```
