# -*- coding: utf-8 -*-
# @time:2019/5/5 16:34
# Author:殇殇
# @file:do_suds.py
# @fuction: 封装请求方法
from suds.client import Client
from common.config import ReadConfig
from common.my_log import MyLog

my_log = MyLog (__name__)

config = ReadConfig ()  # 实例化类


class DoSuds:
    def do_suds(self,method,url,data=None):
        if type(data)==str:
            data = eval(data)
        url = config.get_strvalue('api','pre_url')+url  # 读取配置文件的前半部分
        my_log.info('请求的数据是：{}'.format(data))
        my_log.info('请求的地址是：{}'.format(url))
        client = Client (url)
        if method == 'sendMCode':
            resp = client.service.sendMCode(data)
        elif method == 'userRegister':
            resp = client.service.userRegister(data)
        elif method == 'verifyUserAuth':
            resp = client.service.verifyUserAuth (data)
        else:
            resp = client.service.bindBankCard(data)
        return resp




if __name__ == '__main__':
    t = {"client_ip": "192.168.70.52", "tmpl_id": "1", "mobile": "18871360120"}
    url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'
    result = DoSuds().do_suds('sendMCode',url=url,data=t)
    print('返回的结果是：',result)