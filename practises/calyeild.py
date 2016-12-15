# -*- coding: UTF-8 -*-
from classes import Stock, format
import numpy as np
import os
from datetime import date, timedelta
from dateutil.parser import parse
import sys

datapath = 'formated/SZ#002673.json'
# amount = float(10000)
stock = Stock()


def getFiles(dirname):
    files = None
    for dirpath, dirnames, filenames in os.walk(dirname):
        files = [os.path.join(dirpath, p) for p in filenames if p.endswith('.json')]
    return files


def getDates(arr):
    return [' - '.join([d['date'], str(d['close'])]) for d in arr]


def reformatItem(item, index):
    item['index'] = index
    item['odate'] = parse(item['date']).date()
    return item


result = []


def test(filepath, amount=float(10000), rate=0.1, begdate=date(2016, 1, 1), enddate=date(2017, 1, 1)):
    stock.load(filepath)
    nextDate = begdate
    total = len(stock.items)
    global result
    durs = []
    turnings = [reformatItem(stock.items[i], i) for i in range(1, total - 1)
                if stock.isFirstTurningByMACD(stock.items[i], stock.items[i - 1])]
    for d in [d for d in turnings if d['odate'] >= begdate and d['odate'] < enddate]:
        if d['odate'] < nextDate:
            continue
        if d['odate'] > nextDate:
            nextDate = d['odate']
        # in
        num = int(amount / d['close'])
        for dd in [j for j in stock.items if parse(j['date']).date() > nextDate]:
            diff = dd['high'] - d['close']
            diffp = diff / d['close']
            if diffp >= rate:
                # out
                out = d['close'] * (1 + rate)

                diffout = out - d['close']
                dur = parse(dd['date']) - parse(d['date'])
                durs.extend([dur])
                print('%s - %-5s | %s - %-7s open=%-5s,high=%-5s,close=%-5s | %-6s:%s | %s' % (
                    d['date'], d['close'], dd['date'], out, dd['open'], dd['high'],
                    dd['close'], diffout, num, dur))
                amount += diffout * num
                nextDate = parse(dd['date']).date()
                break
    print('amount = {}'.format(amount))
    result.extend(
        [{'code': stock.code, 'amount': amount, 'durs': durs, 'avgtimes': sum(durs, timedelta()) / len(durs)}])


def hitted(filepath, rate=0.1, begdate=date(2016, 1, 1), enddate=date(2017, 1, 1)):
    stock.load(filepath)
    nextDate = begdate
    total = len(stock.items)

    # durs = []
    turnings = [reformatItem(stock.items[i], i) for i in range(1, total - 1)
                if stock.isFirstTurningByMACD(stock.items[i], stock.items[i - 1])]
    # 有可能已经退市或者其他问题,这类票跳过
    # 没有12月份数据的要跳过
    # 织布机要跳过
    # 没有行情的跳过
    availableTurnings = [d for d in turnings if d['odate'] >= begdate and d['odate'] < enddate]
    if len(availableTurnings) < 3:
        print ('skip %s' % stock.code)
        return (True, stock.code)
    countter = 0
    for d in [d for d in turnings if d['odate'] >= begdate and d['odate'] < enddate]:
        if d['odate'] < nextDate:
            continue
        if d['odate'] > nextDate:
            nextDate = d['odate']
        for dd in [j for j in stock.items if parse(j['date']).date() > nextDate]:
            diff = dd['high'] - d['close']
            diffp = diff / d['close']
            if diffp >= rate:
                # hitted
                countter += 1
                nextDate = parse(dd['date']).date()
                if countter >= 3:
                    return (True, stock.code)
    return (False, stock.code)


def displayResult(arr):
    for d in arr:
        print('%-20s - %-10s' % (d['avgtimes'], d['amount']))


# test(datapath)
files = getFiles('formated')
# for fp in files[:10]:
#     test(fp)
#
# sortedresult = sorted(result, key=lambda d: (d['avgtimes']))
# displayResult(sortedresult)

startYeildRate = 0.1
rateStep = 0.001
lenfiles = len(files)
targetRate = 0
startIndex = 0

for rate in np.arange(0, startYeildRate, rateStep)[::-1]:
    if rate == 0:
        break
    ishit = True
    print('rate = %4s' % (rate))
    i = startIndex
    for fp in files[startIndex:]:
        # print('%-5s / %-5s' % (i, lenfiles))
        sys.stdout.write("\r%5d/%5d   " % (i, lenfiles))
        sys.stdout.flush()
        ishit, code = hitted(fp, rate)
        if not ishit:
            print('not be hitted : %s' % code)
            startIndex = i
            break
        i += 1
    if ishit:
        targetRate = rate
        break
print ('target rate = %s' % (targetRate))

# print(np.arange(0, startYeildRate, rateStep)[::-1])
