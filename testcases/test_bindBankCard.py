# -*- coding: utf-8 -*-
# @time:2019/5/6 14:11
# Author:殇殇
# @file:test_bindBankCard.py
# @fuction: 测试绑定银行卡
import unittest
from ddt import ddt,data
from common.do_excel import DoExcel
from common.contants import *
from common.do_suds import DoSuds
from xml.sax.saxutils import escape
from common.my_log import MyLog

my_log = MyLog (__name__)

do_excel = DoExcel(case_file,'bindBankCard')
bindBankCard_cases = do_excel.get_data()

@ddt
class BindBankCardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        my_log.info('---开始执行测试用例---')
        cls.do_suds = DoSuds ()

    @data(*bindBankCard_cases)
    def test_bindBankCard(self,case):
        my_log.info('开始执行第{}条测试用例：{}'.format(case.case_id,case.title))
        try:
            result = self.do_suds.do_suds (case.method, case.url, case.data)
            print('响应数据：{}'.format(result))
            self.assertEqual (case.expected, escape (result[1]))
            do_excel.write_back (case.case_id + 1, escape (result[1]), 'Pass')
        except AssertionError as e:
            my_log.error('断言失败了：{}'.format(e))
            do_excel.write_back (case.case_id + 1, escape (result[1]), 'Failed')
            raise e

    @classmethod
    def tearDownClass(cls):
        my_log.info('---测试用例执行结束---')


if __name__ == '__main__':
    unittest.main()


