#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:dwb
# datetime:2018/8/7 13:48
# software: PyCharm
# 程序入口

from src.configreader import ConfigReader
from src import globalvar as gol
from src.apitest import TestPlan
import os

gol._init()  # 在主模块进行初始化全局变量
configpath = './config/config.ini'
config = ConfigReader(configpath)
testplan = TestPlan(config.dict)
pass




