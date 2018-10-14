#!/usr/bin/env python
#-*- coding:utf-8 -*-
# author:dwb
# datetime:2018/10/13 11:31
# software: PyCharm

import pymysql
from . import globalvar as gol

class OperationMysql():
    def connect(self, **data):
        self.conn = pymysql.connect(
            host=data['db_host'],
            port=int(data['db_port']),
            user=data['db_user'],
            passwd=data['db_pass'],
            db=data['db_name'],
            charset=data['db_charset'],
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cur = self.conn.cursor()

    # 只获取一条数据
    def getvalue(self, dbkey, sql):
        self.connect(**gol._vars['DB'][dbkey.upper()])
        self.cur.execute(sql)
        sqlresult = self.cur.fetchall()[0]
        if len(sqlresult) > 1:
            raise Exception('sql查询语句返回字段不能超过一个')
        result, = sqlresult.values()
        return result
