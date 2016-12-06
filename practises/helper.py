# -*- coding: UTF-8 -*-
from dateutil.parser import parse
from datetime import datetime
import numpy as np


def getJSONData(path):
    with open(path, 'r') as f:
        lines = f.readlines()
        lines.pop(0)
        lines.pop(0)
        lines.pop(-1)
        return [{'date': parse(data[0]), 'open': float(data[1]), 'high': float(data[2]), 'low': float(data[3]),
                 'close': float(data[4]), 'volume': float(data[5]), 'volumeAmount': float(data[6])} for data in
                (i.replace('\t', ',').replace('\r\n', '').split(',') for i in lines)]


def getData():
    with open('data/SZ#002637.txt', 'r') as f:
        lines = f.readlines()
        print('total:{0}'.format(len(lines)))
        lines.pop(0)
        lines.pop(0)
        lines.pop(-1)
        return [{'date': parse(data[0]), 'open': float(data[1]), 'high': float(data[2]), 'low': float(data[3]),
                 'close': float(data[4])} for data in
                (i.replace('\t', ',').replace('\r\n', '').split(',') for i in lines)]


"""
设向量v(n) n(1~n)
1.求一阶差分向量
  diffv(i)=v(i+1)-v(i) i(1,2,3,...,n-1)
2.对diffv(i)进行符号函数运算得到Trend
  if diffv(i)>0:
    return 1
  elif diffv(i)<0:
    return -1
  else:
    return 0
3.reverse Trend
4.进行如下处理得到R
  if Trend(i)==0 and Trend(i+1)>=0:
    Trend(i)=1
  elif Trend(i)==0 and Trend(i+1)<0:
    Trend(i)=-1
  else:
    Trend(i)=0
5.最后再对R做一次一阶差分向量.波峰:R(i)=-2,位置i+1,波谷R(i)=2,位置i+1
"""


def getPeackAndTrough(values):
    def calTrend(value):
        if value > 0:
            return 1
        elif value < 0:
            return -1
        else:
            return 0

    def calDiffR(value1, value2):
        if value1 == 0 and value2 >= 0:
            return 1
        elif value1 == 0 and value2 < 0:
            return -1
        else:
            return value1

    def findPeackValue(value, index):
        if value == 2:
            return ('speack', value)
        else:
            return ('trough', value)

    diffv = [values[i + 1] - values[i] for i in range(len(values)) if i < len(values) - 1];
    print(diffv)
    trend = [calTrend(v) for v in diffv]
    print (trend)
    r = [calDiffR(trend[i], trend[i + 1]) for i in range(len(trend) - 1)]
    print (r)
    diffr = [r[i + 1] - r[i] for i in range(len(r)) if i < len(r) - 1]
    values = [i + 1 for i in range(len(diffr)) if diffr[i] == 2 or diffr[i] == -2]
    print (values)
    return values
    # diffv=[value[:1]-value for value in values]
