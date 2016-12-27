# -*- coding: UTF-8 -*-
from Stock import Stock
import numpy as np
import os
import json
import sys
import time
import datetime
import matplotlib.pyplot as plt


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


def getFiles(symbols):
    files = getAllFiles()
    result = []
    if not files == None:
        for s in symbols:
            result.extend([fn for fn in files if s in fn])
    return result


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
        # open > 0 volume > 0 排序没有交易的
        # ==curDate 只关注今日
        if stock.length() > 100 and stock.datas[-1]['volume'] > 0 and stock.datas[-1]['date'] == curDate and 0. < \
                stock.datas[-1]['open'] < 100.:
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
    result['up'] = sorted(result['up'], key=lambda d: d['p'])
    result['down'] = sorted(result['down'], key=lambda d: d['p'])
    with open('output/up_down_{:%Y-%m-%d}.json'.format(curDate), 'w+') as f:
        json.dump(result, f)


def generateSummary(curDate=datetime.datetime.today().date()):
    data = getUpDown(curDate)
    if not data == None:
        with open('output/summary_{:%Y-%m-%d}'.format(curDate), 'w+') as f:
            with open('summary.template') as ftemp:
                temp = ftemp.read()
                lup = len(data['up'])
                upp = [d['p'] for d in data['up']]
                ldown = len(data['down'])
                downp = [d['p'] for d in data['down']]
                f.write(temp.format(curDate, lup, min(upp), max(upp), ldown, min(downp), max(downp)))


def getUpDown(curDate=datetime.datetime.today().date()):
    filename = 'output/filter_up_down_{:%Y-%m-%d}.json'.format(curDate)
    with open(filename) as f:
        return json.load(f)
    return None


# def showF1(curDate=datetime.datetime.today().date()):
#     data = getUpDown(curDate)
#     if not data == None:
#         upp = [d['p'] for d in data['up'] if not d['p'] == float('Inf')]
#         downp = [d['p'] for d in data['down'] if not d['p'] == float('Inf')]
#         plt.plot(range(len(upp)), upp)
#         plt.plot(range(len(downp)), downp)
#         plt.show()


# def filter1(curDate):
#     data = getUpDown(curDate)
#     if not data == None:
#         sys.stdout.write('found %s\n' % len(data['up']))
#         symbols = [d['s'] for d in data['up']]
#         files = getFiles(symbols)
#         l = len(files)
#         i = 1
#         result = []
#         for fn in files:
#             sys.stdout.write('\r %s/%s' % (i, l))
#             stock = Stock(fn)
#             if stock.macd[-1] > stock.macd[-2] >= 0:
#                 result.extend([stock.symbol])
#             i += 1
#         return result
#     return None


filter()
generateSummary()