import json
from getJsonData import getJSONData
import os
from datetime import date, datetime

dataPath = 'data/SZ#002637.txt'

fileName, fileExtension = os.path.splitext(os.path.basename(dataPath))

jsonPath = os.path.join('data', '{0}.json'.format(fileName))

jsonData = getJSONData(dataPath)


class ComplexJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, date) or isinstance(o, datetime):
            return o.isoformat()
        else:
            return json.JSONDecoder.default(self, o)

with open(jsonPath, 'w+') as f:
    json.dump(jsonData, f, cls=ComplexJSONEncoder)
