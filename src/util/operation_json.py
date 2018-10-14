#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:dwb
# datetime:2018/9/21 16:58
# software: PyCharm
# 通过jsonpath获取/替换json参数

import os, json, re
from jsonpath_rw import jsonpath, parse
from src.util import globalvar as gol


class JsonReader():
    # 根据json模式获取数据(json模板名:{jsonpath路径，替换字符串})，todo 异常处理
    # 支持jsonpath的'.'  '[n]' 匹配
    def get_json(self, file_path, jsonpattern={}):
        if {} == jsonpattern:
            return jsonpattern
        if os.path.getsize(file_path):
            with open(file_path, encoding='utf-8') as fp:
                templet = list(jsonpattern.keys())[0]
                patterndict = jsonpattern[templet]
                data = json.load(fp)[templet]
                for pat in patterndict:
                    # data = self.pattern_match(data, pat, patterndict[pat])
                    patlist = re.split('(?<=[^\.])\.', pat)
                    if patlist[0] != '$': raise Exception('json提取式必须以$开头')
                    try:
                        data = self.pattern_match(data, patlist, patterndict[pat])
                    except Exception as e:
                        raise Exception('根据替换规则替换json模板失败：%s' % e)
                return data
        else:
            raise Exception('找不到对应的json模板文件')

    # 通过格式修改json,递归逻辑
    def pattern_match(self, tjson, pattern, value):
        if pattern[0] == '$':
            tjson = self.pattern_match(tjson, pattern[1:], value)
        elif 1 < len(pattern):
            if ']' == pattern[0][-1]:  # 支持list，不够专业的处理方式
                subnum = int(pattern[0][-2])
                key = pattern[0][:-3]
                tjson[key][subnum] = self.pattern_match(tjson[key][subnum], pattern[1:], value)
            # if pattern[0][0] == '.':           ..通配符匹配以后再思考
            else:
                tjson[pattern[0]] = self.pattern_match(tjson[pattern[0]], pattern[1:], value)
        else:
            if ']' == pattern[0][-1]:  # 支持list，不够专业的处理方式
                subnum = int(pattern[0][-2])
                key = pattern[0][:-3]
                test = tjson
                tjson[key][subnum] = value
            else:
                tjson[pattern[0]] = value
        return tjson


if __name__ == '__main__':
    jr = JsonReader()
    json = {'quoteDetailIds': ['36904205'], 'invoiceType': 2, 'vinCode': 'L199381', 'carTypeId': 161754, 'bizId': 4140908, 'bizType': 2, 'remark': '', 'factoryType': 0}
    pattern = '$.quoteDetailIds[0]'
    patlist = re.split('(?<=[^\.])\.', pattern)
    json = jr.pattern_match(json, patlist, '@a')
    print(json)
