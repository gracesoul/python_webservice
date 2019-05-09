# -*- coding: utf-8 -*-
# @time:2019/5/6 14:55
# Author:殇殇
# @file:run.py
# @fuction: 执行所有的测试用例


import unittest
from BeautifulReport import BeautifulReport
from common.contants import *

discover = unittest.defaultTestLoader.discover(case_dir,pattern='test_*.py')
BeautifulReport(discover).report(filename='webservice实战测试报告',
                                 description='这是一个包含发送验证码，注册，实名认证和绑定银行卡的测试报告',
                                 report_dir=report_file)


