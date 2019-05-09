# -*- coding: utf-8 -*-
# @time:2019/5/6 14:36
# Author:殇殇
# @file:my_log.py
# @fuction: 封装log日志的操作
import logging
from common.contants import *


class MyLog:
    def __init__(self,name):
        self.name = name

    def my_log(self,level,msg):
        # 创建一个日志收集器
        my_logger = logging.getLogger(self.name)
        # 设置日志收集器的等级
        my_logger.setLevel('DEBUG')
        # 设定日志输出格式
        formatter = logging.Formatter ('%(asctime)s-' '%(name)s-' '[%(levelname)s]-' '[%(filename)s:%(lineno)d]-' '[日志信息]:%(message)s')
        # 设定输出渠道 ---> 控制台
        sh = logging.StreamHandler()
        sh.setLevel('DEBUG')
        sh.setFormatter(formatter)
        # 输出到指定的文件
        fh = logging.FileHandler(mylog_file+'/test.log',encoding='utf-8')
        fh.setLevel('DEBUG')
        fh.setFormatter(formatter)
        # 日志收集器与输出渠道的交接
        my_logger.addHandler(sh)
        my_logger.addHandler(fh)
        if level == 'DEBUG':
            my_logger.debug(msg)
        elif level == 'INFO':
            my_logger.info(msg)
        elif level == 'WARNING':
            my_logger.warning(msg)
        elif level == 'ERROR':
            my_logger.error(msg)
        else:
            my_logger.critical(msg)
        # 清除緩存
        my_logger.removeHandler(sh)
        my_logger.removeHandler(fh)

    def debug(self,msg):
        self.my_log('DEBUG',msg)

    def info(self,msg):
        self.my_log('INFO',msg)

    def warning(self,msg):
        self.my_log('WARNING',msg)

    def error(self,msg):
        self.my_log('ERROR',msg)

    def critical(self,msg):
        self.my_log('CRITICAL',msg)


if __name__ == '__main__':
    log = MyLog (name ='case')
    log.info('测试')


