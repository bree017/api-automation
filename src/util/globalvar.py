#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:dwb
# datetime:2018/10/3 15:49
# software: PyCharm
# 公共变量，在需要用的模块导入,DB等配置数据用大写，@开头的用小写

# 初始化，在main一开始执行，此后无需执行
import re

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

# 变量替换,递归逻辑
def transfer(obj):
    if isinstance(obj, dict):
        for i in obj:
            obj[i] = transfer(obj[i])
    elif isinstance(obj, list):
        for i in obj:
            obj[obj.index(i)] = transfer(i)
    elif isinstance(obj, str):
        obj = str_transfer(obj)
    return obj

# 字符串变量替换
def str_transfer(obj):
    if isinstance(obj, str) and obj.find('@') != -1:
        for var in _vars:
            if obj.lower().find(var.lower()) != -1 and var.upper() != 'DB':
                if obj.lower() == var.lower():  # 如果是数字类型的时候不可通过replace方法进行替换
                    obj = _vars[var]
                else:
                    # obj = obj.replace(var, str(_vars[var.lower()]))   忽略变量大小写
                    test =str(_vars[var.lower()])
                    obj = re.sub(var, str(_vars[var.lower()]), obj, flags=re.IGNORECASE)
                return str_transfer(obj)    # 通过递归的方式貌似简单一点
    return obj

if __name__ == '__main__':
    _init()
    ed={"@a":12,'@b':23,'@c':34}
    for i in ed :
        set_value(i,ed[i])

    jsl={"autoAuditFlag":1,"carTypeId":161754,"inquiryCarTypeId":0,"carTypeDTO":{"carTypeId":'@a',"brandId":1,"brandName":"宝马","carSystemId":366,"carSystem":"X6","subBrandName":"进口宝马"},"inquiryDetailDTOs":[{"attrs":{"inquiryDetailId":0,"partsCode":"41617486754","btrPartsName":"前机盖","colorRemark":"","installNum":"1","features":[],"material":[]},"autoAuditFlag":"1","factoryTypes":[0,1,2],"factoryTypesIndex":[0,1,2],"needNum":1,"partCode":"41617486754","partsName":"前机盖","modifiedPartsName":"前机盖","quoteDetailDTOs":[],"remark":"","pictures":[],"priceOf4s":60,"inquiryDetailEPCPicDTOs":[{"inquiryDetailPicId":0,"inquiryDetailId":0,"picUrl":"http://pic.qipeipu.com/npic/bmw/6ad0953b46a62fdaa8bd3f19bca7958c.png","picType":3,"picOrder":0,"showSupplier":1,"picContent":"车前盖/安装件","picPosition":"01","topLeftX":'@b',"topLeftY":128,"bottomRightX":711,"bottomRightY":160,"createTime":None,"updateTime":None,"status":1,"imageNo":"41_1747","identify":"http://pic.qipeipu.com/npic/bmw/6ad0953b46a62fdaa8bd3f19bca7958c.png"}],"inquiryDetailPhysicalPicDTOs":[],"inquiryDetailId":0,"partsInfoVisible":False,"quoteVisible":True,"limitNum":5,"repeatFlag":False,"secQuoting":False,"trackFlagsDTO":{"epcFlag":0}}],"invoiceType":2,"provinceId":19,"vinCode":"L199391","contacts":"七杀","phone":"@c","inquiryId":0,"insuranceWriteParam":{"insuranceNo":"","clientOrgId":1003246,"clientOrgName":"TEST-庐山","townId":445381102,"countyId":1785,"cityId":445300,"provinceId":19}}
    jsl2 ={"a":'@a'}
    jsl3 = {'a':[{'aa':'@a123@b'},{'b':'@b'}],'b':[1242345,'@c','12312']}
    transfer(jsl)
    pass