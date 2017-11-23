# -*- coding: UTF-8 -*-
"""
Created on 2017年11月10日
@author: Leo
"""

# 第三方库
from flask import Flask, Blueprint
from flask_restful import Api

# 项目内部库
from backend.resources.spider import SpiderList
from backend.resources.spider import SpiderSearch

# 项目版本的URL前缀
version_prefix = "/v1"


# 定义Flask项目
app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# 项目资源模板
api.add_resource(SpiderList, version_prefix + '/spider_list')
api.add_resource(SpiderSearch, version_prefix + '/search')
app.register_blueprint(api_bp)

if __name__ == '__main__':
    app.run(port=8080)
