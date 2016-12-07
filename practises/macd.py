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

close = [i['close'] for i in jsonData][-100:]

macd = stock.macd(np.array(close, dtype=np.float64))

print(len(close), len(macd))
print(macd)
