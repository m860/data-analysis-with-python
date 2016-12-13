# -*- coding: UTF-8 -*-

from classes import Stock, format
import numpy as np

path = 'data/SZ#002637.txt'

# format(path, 'data/SZ#002637.json')
#
stock = Stock()
stock.load('data/SZ#002637.json')
print(stock.code)
print (len(stock.items))
print(stock.canBeEnter())
print ([d for d in stock.items if d['diffv']>=0.5])
