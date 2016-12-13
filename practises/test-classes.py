# -*- coding: UTF-8 -*-

from classes import Stock, format
import numpy as np
import os


# path = 'data/SZ#002637.txt'
#
# # format(path, 'data/SZ#002637.json')
# #
# stock = Stock()
# stock.load('data/SZ#002637.json')
# print(stock.code)
# print (len(stock.items))
# print(stock.canBeEnter())
# print ([d for d in stock.items if d['diffv'] >= 0.5])


def getFiles(dirname):
    files = None
    for dirpath, dirnames, filenames in os.walk(dirname):
        files = [os.path.join(dirpath, p) for p in filenames if p.endswith('.json')]
    return files


files = getFiles('formated')
print(files)
stock = Stock()
enterCodes = []
i = 1
l = len(files)
for f in files:
    print('{2}/{1}determine {0}'.format(f, l, i))
    stock.load(f)
    if stock.canBeEnter():
        enterCodes.extend([stock.code])
    i += 1

print(enterCodes)
