# -*- coding: UTF-8 -*-

from classes import Stock, format
import numpy as np
import os


def getFiles(dirname):
    files = None
    for dirpath, dirnames, filenames in os.walk(dirname):
        files = [os.path.join(dirpath, p) for p in filenames if p.endswith('.json')]
    return files


files = getFiles('formated')
l = len(files)

print('total=', l)

stock = Stock()
i = 1

l1 = []

for f in files:
    print('{2}/{1}determine {0}'.format(f, l, i))
    stock.load(f)

    # macd < 0 and diffv > 0 order by |macd| asc
    itemlen = len(stock.items)
    if itemlen > 0:
        last = stock.items[-1]
        if last['macd'] < 0 and last['diffv'] > 0:
            last['order'] = abs(last['macd'])
            l1.extend([last])

    i += 1

print(np.sort(l1, order='order'))
