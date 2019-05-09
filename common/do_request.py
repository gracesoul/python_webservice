# -*- coding: utf-8 -*-
# @time:2019/4/28 16:40
# Author:殇殇
# @file:do_request.py
# @fuction: 测试数据

from suds.client import Client
# user_url = 'http://120.24.235.105:9010/finance-user_info-war-1.0/ws/financeUserInfoFacade.ws?wsdl'
# client = Client(user_url)
# print(client)
#
# t={"channel_id":"2","ip":"192.168.45.20","mobile":"18871362019","pwd":"123456","user_id":"yh1","verify_code":"273445"}
# result = client.service.userRegister(t)
# print(result)
# print(type(result))
# print(result.retInfo)
from suds.sudsobject import asdict


def recursive_asdict(d):
    """Convert Suds object into serializable format."""
    out = {}
    for k, v in asdict (d).items ():
        if hasattr (v, '__keylist__'):
            out[k] = recursive_asdict (v)
        elif isinstance (v, list):
            out[k] = []
            for item in v:
                if hasattr (item, '__keylist__'):
                    out[k].append (recursive_asdict (item))
                else:
                    out[k].append (item)
        else:
            out[k] = v
    return out



# class WebserviceRequest:
#     headers = {'Content-Type': 'application/soap+xml; charset="UTF-8"'}
#
#     def do_request(self, url, data):
#         if type(data)==str:
#             data = eval(data)
#         client = Client(url)
#         print('请求的数据为：{}'.format(data))
#         print('请求的地址为：{}'.format(url))
#         return client
#
#
# if __name__ == '__main__':
#     pass
    # url = 'http://120.24.235.105:9010/sms-service-war-1.0/ws/smsFacade.ws?wsdl'
    # data = {"client_ip": "192.168.70.52", "tmpl_id": "1", "mobile": "18871362011"}
    # request = WebserviceRequest()
    # result = request.do_request(url=url,data=data,interface_name=sendMCode())
    # # print(result)
    # print ('响应结果：{}'.format (result))
    # print ('结果类型是：', type (result))
