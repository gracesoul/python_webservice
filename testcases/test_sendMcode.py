# -*- coding: utf-8 -*-
# @time:2019/4/29 13:59
# Author:殇殇
# @file:test_sendMcode.py
# @fuction: 测试发送验证码功能


import unittest
from ddt import ddt,data
from common.do_excel import DoExcel
from common.contants import *
from xml.sax.saxutils import escape
from suds import WebFault
import warnings
from common.do_suds import DoSuds
from common.my_log import MyLog
from common.do_mysql import DoMysql



my_log = MyLog (__name__)

do_excel = DoExcel(case_file,'sendMCode')
sendMcode_cases = do_excel.get_data()

headers = {'Content-Type': 'application/soap+xml; charset="UTF-8"'}
@ddt
class SendmcodeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        my_log.info('开始执行测试用例')
        warnings.simplefilter ("ignore", ResourceWarning)
        cls.do_suds = DoSuds()
        cls.mysql = DoMysql ('sms_db_20')

    @data(*sendMcode_cases)
    def test_sendmcode(self,case):
        my_log.info('开始执行第{}条测试用例：{}'.format(case.case_id,case.title))
        # 在请求之前 先判断是否需要执行SQL
        if case.check_sql:
            sql = eval(case.check_sql)['sql1']
            sql_result = self.mysql.fetch_one(sql)
            sendcode_before = sql_result['count(Fmobile_no)']
            print('发送验证码之前，数据库的数据有：{}'.format(sendcode_before))


        if case.data.find('normal_mobile')>-1:
            sql = 'select max(Fmobile_no) from sms_db_20.t_mvcode_info_0 ;' # 查询最大手机号码
            max_phone = self.mysql.fetch_one(sql)
            print(type(max_phone))
            max_phone= max_phone['max(Fmobile_no)']
            max_phone = int(max_phone)+1000
            print('最大的手机号码:{}'.format(max_phone))
            # replace 重新返回一个新的字符串 有返回值  一定要有接收
            case.data = case.data.replace('normal_mobile',str(max_phone))
        try:
            result = self.do_suds.do_suds(case.method,case.url,case.data)
            print('响应数据：{}'.format(result))
            self.assertEqual(case.expected,escape(result[1]))
            do_excel.write_back (case.case_id + 1, escape(result[1]),'Pass')
            # 在请求成功后，判断数据是否发生了改变？
            if case.check_sql:
                sql = eval (case.check_sql)['sql1']
                sql_result = self.mysql.fetch_one (sql)
                sendcode_after = sql_result['count(Fmobile_no)']
                print ('发送验证码之后，数据库的数据有：{}'.format (sendcode_before))
                self.assertEqual(sendcode_before+1,sendcode_after)
        except WebFault as e:
            result = str((e.__dict__)['fault'].faultstring)
            try:
                self.assertEqual(case.expected,result)
                my_log.info ('返回结果是：{}'.format (result))
                do_excel.write_back (case.case_id + 1, result, 'pass')
            except AssertionError as error:
                my_log.error('捕获断言出错：{}'.format(error))
                do_excel.write_back (case.case_id + 1, result, 'Failed')
                raise error

    @classmethod
    def tearDownClass(cls):
        my_log.info('测试用例执行完毕')
        cls.mysql.close()


if __name__ == '__main__':
    unittest.main()