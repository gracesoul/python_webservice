# -*- coding: utf-8 -*-
# @time:2019/5/5 15:05
# Author:殇殇
# @file:test_verifiedUserAuth.py
# @fuction: 测试实名认证的接口

import unittest
from xml.sax.saxutils import escape
from ddt import ddt,data
from common.do_excel import DoExcel
from common.contants import *
from common.do_suds import DoSuds
from suds import WebFault
from common.do_cardid import GetCardid
from common.do_context import replace,Context
from common.do_mysql import DoMysql
import random
import warnings
from common.my_log import MyLog

my_log = MyLog (__name__)

do_excel = DoExcel(case_file,'verifiedUserAuth')
verifiedUserAuth_caces = do_excel.get_data()


@ddt
class VerifiedUserAuthTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.simplefilter ("ignore", ResourceWarning)
        my_log.info('---开始执行测试用例---')
        cls.do_suds = DoSuds ()
        cls.mysql = DoMysql ('user_db')
        cls.card = GetCardid ().gennerator ()

    @data(*verifiedUserAuth_caces)
    def test_verifiedUserAuth(self,case):
        global username
        my_log.info ('开始执行第{}条测试用例:{}'.format (case.case_id,case.title))
        case.data = replace (case.data)
        # 在请求之前，检查是否执行SQL语句
        if case.check_sql:
            sql = eval(case.check_sql)['sql1']
            sql_result = self.mysql.fetch_one (sql)
            auth_before = sql_result['count(Fpk_id)']
            my_log.info ('实名认证之前，数据库的数据有：{}'.format (auth_before))

        # 生成唯一的手机号码（将数据库中最大的手机号+1000） 发生验证码接口--normal_mobile
        if case.data.find('normal_mobile')>-1:
            sql = 'select max(Fmobile_no) from sms_db_20.t_mvcode_info_0 ;'
            max_phone = self.mysql.fetch_one(sql)
            max_phone = int(max_phone['max(Fmobile_no)'])+1000
            case.data = case.data.replace('normal_mobile',str(max_phone))
        # 注册接口 #register_mobile# 将最大的手机号 传到注册接口中
            setattr(Context,'register_mobile',str(max_phone))
        # 保证注册接口的用户名不一样 username (用户名唯一)
        if case.data.find('username')>-1:
            username = getattr(Context,'username')+str(random.randint(1,100))
            case.data = case.data.replace('username',str(username))
            setattr(Context,'username',str(username))

        # 将自动生成的身份证号存在card_id 中
        setattr(Context,'card_id',str(self.card))
        card_id = getattr(Context,'card_id')
        case.data = case.data.replace ('card_id', self.card)
        my_log.info('自动生成的身份证号是：{}'.format(card_id))


        try:
            result = self.do_suds.do_suds (case.method, case.url, case.data)
            print ('响应的结果是：{}'.format (result))
            self.assertEqual (case.expected, escape (result[1]))
            do_excel.write_back (case.case_id + 1, escape (result[1]), 'Pass')

            # 2.从user_db.t_user_info表中，查到Fuid 并替换参数化
            if escape(result[1])=='ok':
                # 1.将发送的验证码 取出来
                mobile = str(getattr(Context,'register_mobile'))
                sql = "select Fverify_code from sms_db_20.t_mvcode_info_0 where Fmobile_no = {} ".format (mobile)
                phone_code = self.mysql.fetch_one(sql)
                phone_code = phone_code['Fverify_code']
                setattr(Context,'phone_code',str(phone_code))
                my_log.info('注册的手机号：{}'.format(mobile))
                my_log.info ('验证码：{}'.format (phone_code))

                # 注册功能后，查询数据库 根据用户名将Fuid 用户id取出来
                username = str(getattr(Context,'username'))
                sql = "select Fuid from user_db.t_user_info where Fuser_id = '{}'".format(username)
                user_id = self.mysql.fetch_one(sql)
                user_id = user_id['Fuid']
                my_log.info('查到的用户id是：{}'.format(user_id))
                setattr(Context,'user_id',str(user_id))

                # 在请求成功之后，检查是否执行SQL语句
                if case.check_sql:
                    sql = eval(case.check_sql)['sql1']
                    sql_result = self.mysql.fetch_one (sql)
                    auth_after = sql_result['count(Fpk_id)']
                    my_log.info ('实名认证之后，数据库的数据有：{}'.format (auth_after))

        except AssertionError as e:
            my_log.error ('断言失败了：{}'.format (e))
            do_excel.write_back (case.case_id + 1, escape (result[1]), 'Failed')
            raise e
        except WebFault as error:
            result = str ((error.__dict__)['fault'].faultstring)
            try:
                print ('返回结果是：{}'.format (result))
                self.assertEqual (case.expected, result)
                do_excel.write_back (case.case_id + 1, result, 'Pass')
            except AssertionError as e:
                my_log.error ('捕获断言失败：{}'.format (e))
                do_excel.write_back (case.case_id + 1, result, 'Failed')
                raise e


    @classmethod
    def tearDownClass(cls):
        cls.mysql.close()
        my_log.info('---测试用例执行结束---')


if __name__ == '__main__':
    unittest.main()


