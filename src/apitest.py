#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:dwb
# datetime:2018/9/21 17:31
# software: PyCharm

import re,json
from src.util.operation_case import CaseReader


class TestCase():
    def __init__(self, **data):
        self.id = data['id']
        self.casename = data['casename']
        self.isactive = ('isactive' in data) and data['isactive'] or 1
        self.platform = ('platform' in data) and data['platform'] or 0
        self.url = data['url']
        self.method = data['method']
        self.header = ('header' in data) and data['header'] or '{}'
        self.cookie = ('cookie' in data) and data['cookie'] or '{}'
        self.param = ('param' in data) and data['param'] or '{}'
        self.body = ('body' in data) and data['body'] or '{}'
        self.expect = ('expect' in data) and data['expect'] or '{}'
        self.response = ('response' in data) and data['response'] or ''
        self.extraction = ('extraction' in data) and data['extraction'] or '{}'
        self.result = ('result' in data) and data['result'] or 0
        self.issuccess = ('issuccess' in data) and data['issuccess'] or 0
        self.start_time = ('start_time' in data) and data['start_time'] or ''
        self.end_time = ('end_time' in data) and data['end_time'] or ''
        self.remark = ('remark' in data) and data['remark'] or ''
        self.convert()

    #testcase数据格式转换
    def convert(self):
        try:
            self.id = int(self.id)
            self.casename = str(self.casename)
            self.platform = int(self.platform)
            self.isactive = (self.isactive in ['0',0,'false','False',False]) and 0 or 1
            self.param = json.loads(self.param)
            self.body = json.loads(self.body)
            self.header = json.loads(self.header)
            self.cookie = json.loads(self.cookie)
            self.expect = json.loads(self.expect)
            self.extraction = json.loads(self.extraction)
        except Exception as e:
            self.isactive = 0
            self.issuccess = -1
            self.result = '数据转换过程错误：%s' % e


    # 变量替换
    def transfer(self):
        pass




class TestSuite():
    def __init__(self, suitname, filepath, case=None, **data):
        self.suitename = ('suitename' in data) and data['suitename'] or ''
        self.caselist = ('caselist' in data) and data['caselist'] or []
        self.start_time = ('start_time' in data) and data['start_time'] or ''
        self.end_time = ('end_time' in data) and data['end_time'] or ''
        self.result = ('result' in data) and data['result'] or 0
        self.remark = ('remark' in data) and data['remark'] or ''

        self.suitename = suitname
        if case:
            self.caselist = self.get_case(case, filepath)

    def get_case(self, caselist, filepath):
        # 预判需要获取哪些sheet的用例
        sheet = []
        for case in caselist:
            pre = re.split('[0-9]', case)[0].lower()
            if pre not in sheet : sheet.append(pre)

        casereader = CaseReader()
        casemap = {}
        for i in sheet:
            casemap[i] = casereader.getsheet(filepath, ord(i)-97)      # 暂时通过abc对应012的方式夺取对应的sheet

        # 从casemap中获取所需要的用例
        res = []
        for case in caselist:
            spot = re.search('[1-9]',case).span()[0]    # 字符串提取，应该有更优雅的方式的
            pre = case[:spot].lower()
            body = case[spot:]
            if body.find('-') != -1:        # 处理以"-"连接的区间
                leftnum , rightnum = body.split('-')
                for i in range(int(leftnum)-1, int(rightnum)):
                    res.append(TestCase(**casemap[pre][i]))
            else:
                res.append(TestCase(**casemap[pre][int(body)-1]))

        return res

    # 执行测试套件
    def runsuite(self):
        runner = HttpHelper()
        runner.sendrequest()


class TestPlan():
    def __init__(self, config, **data):
        self.planname = ('planname' in data) and data['planname'] or ''
        self.suitelist = ('suitelist' in data) and data['suitelist'] or []
        self.start_time = ('start_time' in data) and data['start_time'] or ''
        self.end_time = ('end_time' in data) and data['end_time'] or ''
        self.result = ('result' in data) and data['result'] or 0
        self.remark = ('remark' in data) and data['remark'] or ''

        suitelist = []
        for suitname in config['TESTPLAN']:
            ts = TestSuite(suitname, config['SETTING']['casepath'], config['TESTPLAN'][suitname])
            suitelist.append(ts)
        self.suitelist = suitelist

    # 执行参数计划
    def runplan(self):
        for suite in self.suitelist:
            suite.runsuit()
