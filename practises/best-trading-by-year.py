from classes import Stock, format
import numpy as np
import os
from datetime import date, timedelta
from dateutil.parser import parse
import sys
from multiprocessing import Pool
import time
import json

stock = Stock()
raterange = np.arange(0.02, 0.5, 0.001)[::-1]


def getFiles(dirname):
    files = None
    for dirpath, dirnames, filenames in os.walk(dirname):
        files = [os.path.join(dirpath, p) for p in filenames if p.endswith('.json')]
    return files


files = getFiles('formated')


def getDates(arr):
    return [' - '.join([d['date'], str(d['close'])]) for d in arr]


def reformatItem(item, index):
    item['index'] = index
    item['odate'] = parse(item['date']).date()
    return item


def test(rate, nextdate=date(2016, 1, 1), amount=float(10000)):
    total = len(stock.items)
    durs = []
    turnings = [stock.items[i] for i in range(1, total - 1) if
                stock.isFirstTurningByMACD(stock.items[i], stock.items[i - 1])]
    for d in turnings:
        if d['odate'] < nextdate:
            continue
        if d['odate'] > nextdate:
            nextdate = d['odate']
        # in
        num = int(amount / d['close'])
        for dd in [j for j in stock.items if j['odate'] > nextdate]:
            diff = dd['high'] - d['close']
            diffp = diff / d['close']
            if diffp >= rate:
                # out
                out = d['close'] * (1 + rate)

                diffout = out - d['close']
                dur = parse(dd['date']) - parse(d['date'])
                durs.extend([dur])
                # print('%s - %-5s | %s - %-7s open=%-5s,high=%-5s,close=%-5s | %-6s:%s | %s' % (
                #     d['date'], d['close'], dd['date'], out, dd['open'], dd['high'],
                #     dd['close'], diffout, num, dur))
                amount += diffout * num
                nextdate = dd['odate']
                break

    lendurs = len(durs)
    avg = 0
    if lendurs > 0:
        avg = sum(durs, timedelta()) / lendurs
    return {
        'tradingTimes': lendurs,
        'amount': amount,
        'avgTradingTimes': str(avg),
        'rate': rate
    }


def testWrapper(args):
    return test(*args)


def displayResult(arr):
    for d in arr:
        print('%-20s | %-10s' % (d['avgtimes'], d['amount']))


def fmtitem(item):
    item['odate'] = parse(item['date']).date()
    return item


def run(begindate=date(2016, 1, 1), enddate=date(2017, 1, 1)):
    result = []
    i = 1
    l = len(files)
    start_time = time.time()
    for fp in files:
        stock.load(fp)
        stock.items = [fmtitem(item) for item in stock.items if
                       parse(item['date']).date() >= begindate and parse(item['date']).date() < enddate]
        pool = Pool(10)
        p = pool.map(test, raterange)
        if len(p) > 0:
            sp = sorted(p, key=lambda d: (d['tradingTimes'], d['amount']), reverse=True)
            fir = sp[0]
            fir['code'] = stock.code
            result.extend([fir])
        pool.close()
        sys.stdout.write("\r %s/%s cost %s seconds" % (i, l, (time.time() - start_time)))
        start_time = time.time()
        i += 1

    sr = sorted(result, key=lambda d: (d['tradingTimes'], d['amount']), reverse=True)
    
    # save to file
    with open('output/2016.json','w+') as f:
        json.dump(sr,f)

run()