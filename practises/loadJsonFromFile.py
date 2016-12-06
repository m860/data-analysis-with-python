import json
from getJsonData import getJSONData
import os
from datetime import date, datetime

dataPath = 'data/SZ#002637.txt'

fileName, fileExtension = os.path.splitext(os.path.basename(dataPath))

jsonPath = os.path.join('data', '{0}.json'.format(fileName))


with open(jsonPath, 'r') as f:
    jsonData = json.load(f)
    print(len(jsonData))
    print (jsonData[0])
    print (jsonData[-1])
