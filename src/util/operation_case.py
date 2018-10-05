#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:dwb
# datetime:2018/9/25 14:39
# software: PyCharm

import xlrd
import json,os

class CaseReader():

    #获取整个sheet的用例
    def getsheet(self,file,sheet):
        data=[]
        sheet = xlrd.open_workbook(file,formatting_info=True).sheet_by_index(sheet)
        for i in range(sheet.nrows):
                data.append(sheet.row_values(i))
        res = self.tocase(data)
        return res

    #将excel数据转换成testcase字典
    def tocase(self,data):
        res=[]
        for i in data:
            print (i)
            if i[0] != '' and i != data[0]:
                res.append({
                    'id': i[0],
                    'casename': i[1],
                    'platform': i[2],
                    'url': i[3],
                    'isactive': i[4],
                    'method': i[5],
                    'param': i[6],
                    'body': i[7],
                    'header': i[8],
                    'cookie': i[9],
                    'expect': i[10],
                    'extraction': i[11],
                    'remark': i[11]
                })
        return res




if __name__ == '__main__':
    file='D:/dengwenbin/project/api-automation/case/case.xls'
    sheet=0
    CR=CaseReader()
    data=CR.getsheet(file,sheet)
    pass