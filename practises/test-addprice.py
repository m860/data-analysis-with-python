# -*- coding: UTF-8 -*-

from classes import Stock, format
import numpy as np
import os

format('original/SH#600000.txt', 'formated/SH#600000.json')
stock = Stock()
stock.load('formated/SH#600000.json')
print (len(stock.items))

last = stock.items.pop(-1)
print (last)
stock.addPrice({
    'date': '2016/12/12',
    'open': np.float64(17.34),
    'high': np.float64(17.57),
    'low': np.float64(17.19),
    'close': np.float64(17.49),
    'volume': np.float64(48359554),
    'amount': np.float64(841905152.00)
})
print (stock.items[-1])

