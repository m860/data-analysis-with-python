from Stock import Stock
import numpy as np
import os
import json
import sys


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
for file in files:
    sys.stdout.write('\r%s/%s' % (i, l))
    stock = Stock(file)
    if stock.datas[-1]['volume'] >= 100000:
        if stock.macd[-3] <= stock.macd[-2] <= stock.macd[-1] and stock.macd[-1] >= -0.2:
            result.extend([stock.symbol])
    i += 1

print(result)
