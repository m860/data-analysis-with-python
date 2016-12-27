# -*- coding: UTF-8 -*-
from Stock import Stock
import numpy as np
import os
import json
import sys
import time
import datetime


def getAllFiles(dirname="../sync_data/download"):
    files = None
    for dirpath, dirnames, filenames in os.walk(dirname):
        files = [os.path.join(dirpath, filename) for filename in filenames if
                 filename.startswith('SH') or filename.startswith("SZ")]
    return files


def getFile(symbol):
    files = getAllFiles()
    if not files == None:
        return [filename for filename in files if symbol in filename]
    return None


# s = Stock(getFile("002673")[0])
# with open('002673.json','w+') as f:
#     json.dump(s.__dict__,f)

result = []
files = getAllFiles()
l = len(files)
i = 1
beginTime = time.time()
curDate = datetime.date(2016, 12, 26)
for file in files:
    sys.stdout.write('\r%s/%s \' %s is found \' %s' % (i, l, len(result), time.time() - beginTime))
    stock = Stock(file)
    if stock.length() > 100:
        if stock.datas[-1]['date'] == curDate and stock.datas[-1]['open'] < 1000.:
            if stock.datas[-1]['volume'] >= 100000 and stock.macd[-1] >= 0 and stock.macd[-2] <= stock.macd[-1]:
                result.extend([stock.symbol])
    i += 1
sys.stdout.write('\n')
print(time.time() - beginTime)
with open('output/filter1_{:%Y-%m-%d}.txt'.format(curDate), 'w+') as f:
    f.write('\n'.join(result))
