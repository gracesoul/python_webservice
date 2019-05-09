# -*- coding: utf-8 -*-
# @time:2019/5/9 8:20
# Author:殇殇
# @file:do_cardid.py
# @fuction: 自动生成身份证号

from datetime import date
from datetime import timedelta
import random
from common.contants import cardid_dir

class GetCardid:
    def getdistrictcode(self):
        codelist = []
        file = open (cardid_dir)
        lines = file.readlines ()  # 逐行读取
        for line in lines:
            if line.lstrip ().rstrip ().strip () != '' and (line.lstrip ().rstrip ().strip ())[:6][
                                                           -2:] != '00':  # 如果每行中去重后不为空，并且6位数字中最后两位不为00，则添加到列表里。（最后两位为00时为省份或地级市代码）
                codelist.append (line[:6])  # print(line[:6])  # print(codelist)
        return codelist


    def gennerator(self):
        codelist = self.getdistrictcode ()
        id = codelist[random.randint (0, len (codelist))]  # 地区项
        id = id + str (random.randint (1950, 1998))  # 年份项
        da = date.today () + timedelta (days=random.randint (1, 366))  # 月份和日期项
        id = id + da.strftime ('%m%d')
        id = id + str (random.randint (100, 300))  # ，顺序号简单处理

        i = 0
        count = 0
        weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
        checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3',
                     '10': '2'}  # 校验码映射
        for i in range (0, len (id)):
            count = count + int (id[i]) * weight[i]
        id = id + checkcode[str (count % 11)]  # 算出校验码
        return id


if __name__ == '__main__':
    # print (gennerator ())
    cardid = GetCardid ()
    id = cardid.gennerator()
    print(id)


