#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018/6/3 0003 下午 5:57
# @Author  : bree
# @Site    : 
# @File    : sender.py
# @Software: PyCharm
import requests
import datetime,sys,json,re,os
from apps.interfacetest.apitest.jsoncheck import JsonCheck
from django.template import Context, loader
from django.conf import settings
import codecs

class HttpHelper():
    def __int__(self):
        self.s = requests.Session()

    def sendrequest(caselist):
        s = requests.Session()
        for testcase in caselist:
            try:
                url = testcase["url"]
                headers = testcase["header"] != '' and json.loads(testcase["header"]) or ''
                cookies = testcase["cookie"] != '' and json.loads(testcase["cookie"]) or ''
                params = testcase["param"] != '' and json.loads(testcase["param"]) or ''
                try:
                    bodytype = json.loads(testcase["body"])['type']
                    body = json.loads(testcase["body"])['data']
                except:
                    bodytype = ''
                    body = ''
                testcase["start_time"]=datetime.datetime.now()
                if testcase["method"].lower()=='post':
                    rsp = s.post(url,params=params,data=body,headers=headers,cookies=cookies)
                elif testcase["method"].lower()=='get':
                    rsp = s.get(url, params=params, data=body, headers=headers, cookies=cookies)
                else:
                    testcase["result"]='不支持的method'
                    testcase["issuccess"] = 0
                    return
                testcase["end_time"] = datetime.datetime.now()
                try:        #优先json（text有编码问题）
                    testcase["response"]= rsp.json()
                except Exception as e:
                    testcase["response"] = rsp.text()
                if rsp.status_code != 200:
                    testcase["issuccess"] = 0
                    testcase["result"]='接口返回状态码：%s'%(rsp.status_code)
                else:
                    testcase["issuccess"] = 1
                    expect=testcase["expect"] != '' and json.loads(testcase["expect"]) or ''
                    jsoncheck = JsonCheck()
                    for i in expect:
                        try:
                            if i=='*':      #如果key是*就是表示从结果中搜索字符串（正则方式）--目前无法传多个，需要改成list
                                testcase["issuccess"] = 1 if re.search(expect[i], str(testcase["response"])) else 0
                                if testcase["issuccess"] != 1:
                                    testcase["result"] = '%s:%s--没有匹配的数据' % (i, expect[i])
                                    break
                            else:
                                #转换特殊类型
                                if expect[i].lower() in ['none','null']:
                                    exp = None
                                elif expect[i].lower() in ['true']:
                                    exp = True
                                elif expect[i].lower() in ['false']:
                                    exp = False
                                else:exp = expect[i]
                                testcase["issuccess"],testcase["result"] = jsoncheck.json_reg(i,exp,testcase["response"])
                                if testcase["issuccess"]==2: testcase["issuccess"], testcase["result"]=0,'响应数据不是JSON格式'
                                if testcase["issuccess"] != 1: break
                        except Exception as e:
                            testcase["issuccess"] = 0
                            testcase["result"] = '%s:%s匹配异常--%s' % (i, expect[i],e)
                            break
                    if testcase["issuccess"] == 1:testcase["result"]="验证通过"
            except Exception as e:
                testcase["result"] = '调用接口异常：'+str(e)
                testcase["issuccess"] = 0

    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except Exception as e:
            return False
        return True

    #发送请求,params为url参数，body为请求体
    def sender(url,methon,params={},body={},headers={},cookies={}):
        if 'POST' == methon.upper():
            rsp = s.post(url,params=params,data=body,headers=headers,cookies=cookies)
        elif 'GET' == methon.upper():
            rsp = s.get(url, params=params,data=body, headers=headers, cookies=cookies)
        else:
            raise Exception('不支持的请求方法：%s' %methon)
        return rsp





if __name__=='__main__':

    # tc={
    #     'method':'post',
    #     'param':'{"type":"testcase","ids":"29"}',
    #     'header':'{"test":"123"}',
    #     'body':'{"type":"application/json","data":"123"}',
    #     'cookie':'{"123":"234"}',
    #     'expect':'{"*":"登录1"}',
    #     'url':'http://gz.ews.sellercube.com'
    # }
    # testcaselist=[tc]
    # www=json.loads(tc.body)
    # sendrequest(testcaselist)
    # print(testcaselist[0])
    testplan=''
    createreport(testplan)