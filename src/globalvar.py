#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:dwb
# datetime:2018/10/3 15:49
# software: PyCharm

def _init():
    global _vars
    _vars = {}

def set_value(key,value):
    # 定义一个全局变量
    _vars[key] = value

def get_value(key,defValue=None):
    # 获得一个全局变量,不存在则返回默认值
    try:
        return _vars[key]
    except KeyError:
        return defValue

#def transfer():