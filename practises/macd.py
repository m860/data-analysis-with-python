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

num = 100

close = np.array([i['close'] for i in jsonData][-num:], dtype=np.float64)

ema12 = stock.ema(close, 12)
ema26 = stock.ema(close, 26)
macd = stock.macd(close)

plt.bar(range(num), macd)
plt.plot(range(num), ema12, 'r-')
plt.plot(range(num), ema26, 'g-')
plt.show()
