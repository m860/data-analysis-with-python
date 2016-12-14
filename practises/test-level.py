# -*- coding: UTF-8 -*-

from classes import Stock, format
import numpy as np
import os


def getFiles(dirname):
    files = None
    for dirpath, dirnames, filenames in os.walk(dirname):
        files = [os.path.join(dirpath, p) for p in filenames if p.endswith('.json')]
    return files


def getCode(arr):
    return [d['code'] for d in arr]


def output(title, arr, path='output/result.txt'):
    with open(path, 'a') as f:
        f.write('{0}:{1}\n'.format(title, ','.join(getCode(arr))))


files = getFiles('formated')
l = len(files)

print('total=', l)

stock = Stock()
i = 1

# stock.load(files[0])
# ordered=sorted(stock.items,key=lambda d:d['close'],reverse=True)
# print(ordered[:2])
# 即将反转
l1 = []
# 已反转
l2 = []

for f in files:
    print('{2}/{1}determine {0}'.format(f, l, i))
    stock.load(f)
    # macd < 0 and diffv > 0 order by |macd| asc
    itemlen = len(stock.items)
    if itemlen > 0:
        last = stock.items[-1]
        last['code'] = stock.code
        if last['volume'] > 0 and not stock.blocked():
            if last['macd'] < 0 and last['diffv'] > 0:
                last['order'] = abs(last['macd'])
                l1.extend([last])
            if stock.isFirstTurningByMACD():
                l2.extend([last])

    i += 1

# 即将反转
l1sorted = sorted(l1, key=lambda d: d['order'], reverse=True)
# 即将反转 & 相对低位
l11 = [d for d in l1sorted if d['diff'] <= 0]
# 即将反转 & 相对低位 & 涨势很明显
l12 = [d for d in l1sorted if d['diff'] <= 0 and d['diffv'] >= 1]

l2sorted = sorted(l2, key=lambda d: d['macd'])

outputpath = 'output/result.txt'
if os.path.exists(outputpath):
    os.remove(outputpath)

output('即将反转', l1sorted, outputpath)
output('即将反转 & 相对低位', l11, outputpath)
output('即将反转 & 相对低位 & 涨势很明显', l12, outputpath)
output('已反转', l2sorted, outputpath)
