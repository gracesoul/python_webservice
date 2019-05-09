# -*- coding: utf-8 -*-
# @time:2019/5/8 14:03
# Author:殇殇
# @file:do_context.py
# @fuction: 封装操作正则匹配  将配置文件的数据 进行替换
import re
from common.config import ReadConfig
import configparser
config = ReadConfig () # 实例化


class Context:
    register_mobile = None
    phone_code = None
    username= 'sandy'
    card_id=None


# 使用正则进行将参数化的值进行替换
def replace(data):
    p = '#(.*?)#'
    while re.search(p,data):
        find_origin_data = re.search(p,data) # 找到就返回匹配对象，如果没有找到匹配，则为None
        find_key = find_origin_data.group(1) # 取出key值(group(1)只返回指定组的内容)
        try:
            find_value = config.get_strvalue('data',find_key) # 在配置文件中，通过key值取出value值
        except configparser.NoOptionError as e:
            # 如果在配置文件里面没有找到，就在Context类里面找
            if hasattr(Context,find_key):
                find_value = getattr(Context,find_key)
            else:
                print('找不到参数化的值')
                raise e
        data = re.sub(p,find_value,data,count=1) # count 替换的次数
    return data

