# -*- coding: utf-8 -*-
# @time:2019/5/7 14:25
# Author:殇殇
# @file:config.py
# @fuction: 读取配置文件

from configparser import ConfigParser
from common.contants import test_dir


class ReadConfig:

    def __init__(self,encoding='utf-8'):
        # 1.打开配置文件
        self.cf = ConfigParser ()
        # 2.加载配置文件
        self.cf.read(test_dir,encoding)

    def get_intvalue(self,section,option):
        return self.cf.getint(section,option)

    def get_boolvalue(self,section,option):
        return self.cf.getboolean(section,option)

    def get_strvalue(self,section,option):
        return self.cf.get(section,option)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self,section):
        return self.cf.options(section)

if __name__ == '__main__':
    config = ReadConfig()
    result = config.get_strvalue('api','pre_url')
    print(result)


