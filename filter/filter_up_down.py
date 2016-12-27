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


def filter(curDate=datetime.datetime.today().date()):
    result = {
        'up': [],
        'down': []
    }
    files = getAllFiles()
    l = len(files)
    i = 1
    beginTime = time.time()
    for file in files:
        sys.stdout.write(
            '\r%s/%s up=%s down=%s %s' % (i, l, len(result['up']), len(result['down']), time.time() - beginTime))
        sys.stdout.flush()
        stock = Stock(file, cal=False)
        # > 100 排除新股
        # open < 100 排除指股
        # ==curDate 排除停牌的或者其他
        if stock.length() > 100 and stock.datas[-1]['date'] == curDate and stock.datas[-1]['open'] < 100.:
            if stock.datas[-1]['close'] > stock.datas[-1]['open']:
                result['up'].extend([{
                    's': stock.symbol,
                    'p': (stock.datas[-1]['close'] - stock.datas[-1]['open']) / stock.datas[-1]['open']
                }])
            if stock.datas[-1]['close'] < stock.datas[-1]['open']:
                result['down'].extend([{
                    's': stock.symbol,
                    'p': (stock.datas[-1]['close'] - stock.datas[-1]['open']) / stock.datas[-1]['open']
                }])
        i += 1
    with open('output/filter_up_down_{:%Y-%m-%d}.json'.format(curDate), 'w+') as f:
        json.dump(result, f)


filter(datetime.date(2016, 12, 26))
