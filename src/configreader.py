#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:dwb
# datetime:2018/10/3 15:32
# software: PyCharm
from . import globalvar as gol

import configparser,itertools,re
from src import globalvar as gol

class ConfigReader():
    def __init__(self, path):
        self.path = path
        self.dict = {}
        self.config = configparser.ConfigParser()
        self.config.read(path, 'UTF-8')
        self.to_dict()
        self.db_transfer()
        self.gol_transfer()


    # 将数据转换为字典
    def to_dict(self):
        res = {}
        for s in self.config.sections():
            keys = {}
            for k in self.config.options(s):
                # 测试用例特殊处理，转换为list
                if 'TESTPLAN' == s:
                    keys[k] = self.config[s][k].split(',')
                else:
                    keys[k] = self.config[s][k]
            res[s] = keys
        self.dict = res


    # 提取数据库配置,存放到公共变量中
    def db_transfer(self):
        res = {}
        for s in self.dict:
            if s.find('DB-') != -1:
                res[s[3:]] = self.dict[s]
        gol.set_value('DB',res)

    # 将预置环境变量放到公共变量中
    def gol_transfer(self):
        for s in self.dict['GLOBALS']:
            gol.set_value(s, self.dict['GLOBALS'][s])


