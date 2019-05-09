# -*- coding: utf-8 -*-
# @time:2019/5/7 15:09
# Author:殇殇
# @file:do_mysql.py
# @fuction: 封装数据库的操作

import pymysql
from common.config import ReadConfig

config = ReadConfig ()


class DoMysql:
    '''
    1.建立连接，数据库的连接信息
    2.新建查询页面
    3.编写SQL语句
    4.执行sql语句
    5.查看结果
    6.关闭查询
    7.关闭数据库的连接
    '''
    def __init__(self,db_name):
        db_host = config.get_strvalue('db_test','db_host')
        db_username = config.get_strvalue('db_test','db_username')
        db_password = config.get_strvalue ('db_test', 'db_password')
        self.db_name = db_name
        db_port = config.get_intvalue ('db_test', 'db_port')
        self.db = pymysql.connect(host=db_host,user=db_username,
                        password=db_password,database=self.db_name,port=db_port,charset = 'utf8')
        # 使用 cursor() 方法创建一个游标对象 cursor 设置返回字典
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor) # 创建字典形式的游标

    def fetch_one(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
        return self.cursor.fetchone()

    def fetch_all(self,sql):
        self.cursor.execute(sql)
        self.db.commit()
        self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.db.close()

if __name__ == '__main__':
    mysql = DoMysql ('sms_db_20')
    sql = 'select max(Fmobile_no) from sms_db_20.t_mvcode_info_0 ;'
    result = mysql.fetch_one(sql)
    print(type(result))
    print(result)









