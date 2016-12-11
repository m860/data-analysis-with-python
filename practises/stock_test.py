import json
from getJsonData import getJSONData
import os
from datetime import date, datetime
import numpy as np
import stock
import matplotlib.pyplot as plt

dataPath = 'data/SZ#002637.txt'

fileName, fileExtension = os.path.splitext(os.path.basename(dataPath))

jsonPath = os.path.join('data', '{0}.json'.format(fileName))

jsonData = getJSONData(dataPath)

close = np.array([i['close'] for i in jsonData], dtype=np.float64)

print('total={0}'.format(close.size))

print('2016-11-21:')

ma5 = stock.ma(close, 5)
print('ma5={0}'.format(ma5[-1]))

ma10 = (stock.ma(close, 10))
print('ma10={0}'.format(ma10[-1]))

ma20 = (stock.ma(close, 20))
print('ma20={0}'.format(ma20[-1]))

ma30 = (stock.ma(close, 30))
print('ma30={0}'.format(ma30[-1]))

ma60 = (stock.ma(close, 60))
print('ma60={0}'.format(ma60[-1]))

ema5 = stock.ema(close, 5)
print('ema5={0}'.format(ema5[-1]))

ema10 = stock.ema(close, 10)
print('ema10={0}'.format(ema10[-1]))

ema20 = stock.ema(close, 20)
print('ema20={0}'.format(ema20[-1]))

ema60 = stock.ema(close, 60)
print('ema60={0}'.format(ema60[-1]))

macd,diff,dea = stock.macd(close)
print('macd={0}'.format(macd[-1]))
print('diff={0}'.format(diff[-1]))
print('dea={0}'.format(dea[-1]))
