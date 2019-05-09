# -*- coding: utf-8 -*-
# @time:2019/4/29 14:18
# Author:殇殇
# @file:contants.py
# @fuction: 记录一些重要的文件路径

import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_dir)  # F:\work\python_web
case_file = os.path.join(base_dir,'data','case.xlsx')
# print(case_file) # F:\work\python_web\data\case.xlsx

mylog_file = os.path.join(base_dir,'log')
case_dir = os.path.join(base_dir,'testcases')
report_file = os.path.join(base_dir,'report')
test_dir = os.path.join(base_dir,'config','test.cfg')
cardid_dir = os.path.join(base_dir,'config','districtcode.txt')