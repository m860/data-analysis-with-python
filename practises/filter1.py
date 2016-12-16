from classes import Stock, format
import numpy as np
import os
from datetime import date, timedelta
from dateutil.parser import parse
import sys
from multiprocessing import Pool
import time
import json


def getFiles(dirname='formated'):
    files = None
    for dirpath, dirnames, filenames in os.walk(dirname):
        files = [os.path.join(dirpath, p) for p in filenames if p.endswith('.json')]
    return files


def fmtItem(item):
    item['odate'] = parse(item['date']).date()
    return item


def findLatestRecords(stock, curdate):
    return [fmtItem(d) for d in stock.items if
            parse(d['date']).date() <= curdate and parse(d['date']).date() > curdate + timedelta(days=-5)]


def findBestItem(turnings):
    pass


def inCase1(items, preoutpos, preinpos):
    item = items[-1]
    macd = item['macd']
    volume = item['volume']
    ema5 = item['ema5']
    ema10 = item['ema10']
    ema20 = item['ema20']
    low = item['low']
    diff = item['diff']
    close = item['close']
    if macd > 0 and volume > 0 and low > ema5 > ema10 > ema20:
        return True
    return False


def inCase2(items, preoutpos, preinpos):
    item = items[-1]
    if item['diffv'] > 0 and item['deav'] > 0 and item['diff'] >= item['dea'] and item['macdv'] > 0:
        return True
    return False


def outCase1(items, preoutpos, inpos):
    item = items[-1]
    outPrice = inpos['close'] * (0.03 + 1)
    if item['low'] <= outPrice <= item['high']:
        return (True, outPrice)
    elif item['low'] >= outPrice:
        return (True, item['low'])
    return (False, outPrice)


def outCase2(items, preoutpos, inpos):
    matchOutCase1, outprice = outCase1(items, preoutpos, inpos)
    if matchOutCase1:
        if items[-2]['diffv'] <= 0:
            return (True, outprice)
        else:
            return (False, 0)
    return (False, 0)


def run(inCase, outCase=outCase1, begindate=date(2016, 1, 1), enddate=date(2016, 12, 12)):
    print('run %s %s' % (inCase.__name__, outCase.__name__))
    dateRange = np.arange(begindate, enddate).astype(date)
    stock = Stock()
    stock.load('formated/SZ#002673.json')
    stock.items = [fmtItem(d) for d in stock.items]

    # 0:empty,1:full
    state = 0

    repository = 0

    amount = float(10000)

    inPos = None

    outPos = None

    for curdate in dateRange:

        matches = [d for d in stock.items if d['odate'] <= curdate]
        if len(matches) > 0:
            curitem = matches[-1]
            if state == 1:
                # determine whether to out
                canOut, outPrice = outCase(matches, outPos, inPos)
                if canOut:
                    state = 0
                    amount += repository * outPrice
                    percent = ((outPrice - inPos['close']) / inPos['close']) * 100
                    repository = 0
                    print ('%s out : %s (%s%%) , %-5s , %s' % (curdate, outPrice, percent, amount,
                                                               curitem['odate'] - inPos['odate']))
                    outPos = curitem
                continue
            if inCase(matches, outPos, inPos):
                state = 1
                repository = int(amount / curitem['close'])
                amount -= repository * curitem['close']
                inPos = curitem
                print (
                    '%s in  : %-8f(open=%-8f,high=%-8f,low=%-8f) , %-4s , ma5=%-5s ma10=%-5s ma30=%-5s diff=%s,diffv=%s,dea=%s,deav=%s' % (
                        curdate, curitem['close'], curitem['open'], curitem['high'], curitem['low'], repository,
                        curitem['ma5'],
                        curitem['ma10'], curitem['ma30'], curitem['diff'], curitem['diffv'], curitem['dea'],
                        curitem['deav']))
    print('amount = %s , %s%%' % (amount, ((amount - 10000) / 10000) * 100))


def raising(items):
    if items[-1]['macd'] >= items[-2]['macd'] >= items[-3]['macd']:
        return True
    return False


def overThreshold(items, value=-0.2):
    if items[-1]['macd'] >= value:
        return True
    return False


def getLatestReverseMACDDuration(items):
    i = 0
    # 0:init,1:start,2:stop
    status = 0
    for item in reversed(items):
        if status == 0:
            if item['macd'] <= 0:
                status = 1
                i += 1
        else:
            if item['macd'] <= 0:
                i += 1
            else:
                break
    return i


def getLatestReverseMACDDiffRate(items):
    closes = []
    # 0:init,1:start,2:stop
    status = 0
    for item in reversed(items):
        if status == 0:
            if item['macd'] <= 0:
                status = 1
                closes.extend([item['close']])
        else:
            if item['macd'] <= 0:
                closes.extend([item['close']])
            else:
                break
    minc = min(closes)
    maxc = max(closes)
    diff = maxc - minc
    return diff / minc


def getLatestMACDDuration(items):
    i = 0
    # 0:init,1:start
    status = 0
    for item in reversed(items):
        if status == 0:
            if item['macd'] > 0:
                status = 1
                i += 1
            else:
                break
        else:
            if item['macd'] <= 0:
                break
            else:
                i += 1
    return i


# filter 2016/12/12,cal range before 2016/12/12 begin is 2016/12/09
def run():
    files = getFiles()
    filelen = len(files)
    i = 0
    stock = Stock()
    result = []
    for fp in files:
        sys.stdout.write('\r%s/%s' % (i, filelen))
        stock.load(fp)
        stock.items = stock.items[-100:]
        if overThreshold(stock.items) and raising(stock.items):
            data = {
                'code': stock.code,
                'diffRate': getLatestReverseMACDDiffRate(stock.items),
                'macdDuration': getLatestMACDDuration(stock.items)
            }
            result.extend([data])
        i += 1
    sr = sorted(result, key=lambda d: (d['macdDuration'], -d['diffRate']))
    with open('output/filter1.json', 'w+') as f:
        json.dump(sr, f)


run()
