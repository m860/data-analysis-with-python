import json
from getJsonData import getJSONData
import os
from datetime import date, datetime
import numpy as np
import stock

dataPath = 'data/SZ#002637.txt'

fileName, fileExtension = os.path.splitext(os.path.basename(dataPath))

jsonPath = os.path.join('data', '{0}.json'.format(fileName))

jsonData = getJSONData(dataPath)

closes = [i['close'] for i in jsonData[-100:]]
dates = [i['date'] for i in jsonData[-100:]]


ema = stock.ema(np.array(closes, dtype=np.float64))

result=[{dates[i].strftime('%Y%m%d'):ema[i]} for i in range(len(closes))]

print(len(closes), len(ema))
print(result)
