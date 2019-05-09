# -*- coding: utf-8 -*-
# @time:2019/5/5 14:27
# Author:殇殇
# @file:test_userRegister.py
# @fuction: 测试注册接口

import unittest
from ddt import ddt,data
from common.do_excel import DoExcel
from common.contants import *
from xml.sax.saxutils import escape
import warnings
from common.do_suds import DoSuds
from common.do_mysql import DoMysql
from common.do_context import Context,replace
from common.config import ReadConfig
import random
from common.my_log import MyLog

my_log = MyLog (__name__)

config = ReadConfig ()

do_excel = DoExcel(case_file,'userRegister')
sendMcode_cases = do_excel.get_data()

headers = {'Content-Type': 'application/soap+xml; charset="UTF-8"'}
@ddt
class RegisterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter ("ignore", ResourceWarning)
        my_log.info('---开始执行测试用例---')
        cls.do_suds = DoSuds()
        cls.mysql = DoMysql ('sms_db_20')

    @data(*sendMcode_cases)
    def test_register(self,case):
        global username
        my_log.info('开始测试第{}条测试用例：{}'.format(case.case_id,case.title))

        # 在请求之前，先判断是否需要执行SQL
        if case.check_sql:
            sql = eval(case.check_sql)['sql1']
            sql_result = self.mysql.fetch_one(sql)
            before_register = sql_result['count(Fuid)']
            my_log.info('在注册之前，数据库的数据有：{}'.format(before_register))

        case.data = replace (case.data)
        if case.data.find('normal_mobile')>-1:
            sql = 'select max(Fmobile_no) from sms_db_20.t_mvcode_info_0 ;'
            max_phone = self.mysql.fetch_one(sql)
            max_phone = max_phone['max(Fmobile_no)']
            max_phone= int(max_phone)+1000
            my_log.info('最大的手机号是：{}'.format(max_phone))
            case.data = case.data.replace('normal_mobile',str(max_phone))
            setattr(Context,'register_mobile',str(max_phone))
            # 保证用户名不一致
        if case.data.find ('username') > -1:
            username = getattr(Context,'username')
            username = username+str(random.randint(1,100))
            case.data = case.data.replace ('username', str (username))
            setattr(Context,'username',username)
            my_log.info('username的值:{}'.format(username))



        try:
            result = self.do_suds.do_suds (case.method, case.url, case.data)
            print('响应数据：{}'.format(result))
            self.assertEqual (case.expected, escape (result[1]))
            do_excel.write_back (case.case_id + 1, escape (result[1]), 'Pass')
            if escape(result[1])=='ok':
            # 判断验证码发送成功后，查询数据库 取到验证码
                mobile = getattr(Context,'register_mobile')
                mobile = str(mobile)
                sql = "select Fverify_code from sms_db_20.t_mvcode_info_0 where Fmobile_no = {} ".format(mobile)
                # print('sql转换后的值：{}'.format(sql))
                phone_code = self.mysql.fetch_one(sql)
                print('得到的数据是：{}'.format(phone_code))
                phone_code = phone_code['Fverify_code']
                print('得到的验证码是：{}'.format(phone_code))
                setattr(Context,'phone_code',str(phone_code))

                # 在请求成功后，检验是否执行SQL语句
                if case.check_sql:
                    sql = eval(case.check_sql)['sql1']
                    sql_result = self.mysql.fetch_one(sql)
                    register_after = sql_result['count(Fuid)']
                    print ('在注册之前，数据库的数据有：{}'.format (register_after))
                    self.assertEqual(before_register+1,register_after)

        except AssertionError as e:
            my_log.error('断言失败了：{}'.format(e))
            do_excel.write_back (case.case_id + 1, escape (result[1]), 'Failed')
            raise e

    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()
        my_log.info('---测试用例执行结束---')


if __name__ == '__main__':
    unittest.main()
