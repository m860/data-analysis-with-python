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

closes = [i['close'] for i in jsonData[-100:]]
print(closes)
dates = [i['date'] for i in jsonData[-100:]]
print(dates)

ema = stock.ema(np.array(closes, dtype=np.float64))
print(ema)
plt.plot(range(100),ema)
plt.show()
# result=[{dates[i].strftime('%Y%m%d'):ema[i]} for i in range(len(closes))]

# print(len(closes), len(ema))
# print(result)
