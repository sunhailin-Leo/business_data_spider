# 政务数据爬虫

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
```

* 单个爬虫

```Python
# 可以先使用以下命令查看当前有哪些爬虫
scrapy list

# 然后选择一个执行
scrapy crawl <你选择的爬虫名称>

```