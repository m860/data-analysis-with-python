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


def calMA(data, day=5):
    closes = [item['close'] for item in data]
    return [{
                'date': data[i]['date'],
                'ma' + str(day): np.sum(closes[i - day:i]) / day
            } for i in range(day, len(data))]


md5 = calMA(jsonData)
print (len(md5))
print(md5[-1])
md10 = calMA(jsonData, 10)
print (md10[-1])

md52 = stock.ma(np.array([item['close'] for item in jsonData],dtype=np.float64))
print (md52[-1])
