#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:dwb
# datetime:2018/9/21 16:58
# software: PyCharm
# 通过jsonpath获取/替换json参数

import os, json

class JsonReader():
    # 根据json模式获取数据(json模板名:{jsonpath路径，替换字符串})，todo 异常处理
    def get_json(self, file_path, pattern = {}):
        if os.path.getsize(file_path):
            with open(file_path, encoding='utf-8') as fp:
                templet = list(pattern.keys())[0]
                data = json.load(fp)
                data = data[]


                return data
        else:
            return None
