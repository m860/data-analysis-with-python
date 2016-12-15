from classes import Stock, format
import numpy as np
import os
from datetime import date, timedelta
from dateutil.parser import parse
import sys

# datapath = 'formated/SZ#002673.json'
datapath = 'formated/SH#600007.json'
# datapath = 'formated/SZ#000553.json'
# amount = float(10000)

stock = Stock()


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


# result = []

# amounts = []


def test(filepath, amount=float(10000), rate=0.1, begdate=date(2016, 1, 1), enddate=date(2017, 1, 1)):
    stock.load(filepath)
    nextDate = begdate
    total = len(stock.items)
    # print('rate = %s' % rate)
    # global result
    # global amounts
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
                # print('%s - %-5s | %s - %-7s open=%-5s,high=%-5s,close=%-5s | %-6s:%s | %s' % (
                #     d['date'], d['close'], dd['date'], out, dd['open'], dd['high'],
                #     dd['close'], diffout, num, dur))
                amount += diffout * num
                nextDate = parse(dd['date']).date()
                break
    # print('amount = {}'.format(amount))
    # lendurs = len(durs)
    # if not lendurs == 0:
    #     result.extend(
    #         [{'code': stock.code, 'amount': amount, 'durs': durs, 'avgtimes': sum(durs, timedelta()) / len(durs)}])
    # result.extend([{'code': stock.code, 'amount': amount, 'durs': durs, 'avgtimes': timedelta()}])
    # sortedDurs = sorted(durs, reverse=True)
    # if len(sortedDurs) > 0:
    #     d = sortedDurs[0]
    #     return {
    #         'code': stock.code,
    #         'rate': rate,
    #         'amount': amount,
    #         'period': d
    #     }
    # return None
    lendurs = len(durs)
    avg = 0
    if lendurs > 0:
        avg = sum(durs, timedelta()) / lendurs
    return {
        'times': lendurs,
        'amount': amount,
        'avgtime': avg,
        'rate': rate
    }


def displayResult(arr):
    for d in arr:
        print('%-20s | %-10s' % (d['avgtimes'], d['amount']))


# test(datapath)
# for fp in files[:10]:
#     test(fp)

result = []

lenfile = len(files)
i = 1

for fp in files:
    periods = []

    for rate in np.arange(0.02, 0.1, 0.001)[::-1]:
        d = test(fp, rate=rate)
        periods.extend([d])
        sys.stdout.write('\r%4d/%4d %5f' % (i,lenfile,rate))
        sys.stdout.flush()

    sp = sorted(periods, key=lambda d: (d['times'], d['amount']), reverse=True)
    if len(sp) > 0:
        first = sp[0]
        first['code'] = stock.code
        result.extend([first])
    i+=1

sr = sorted(result, key=lambda d: (d['times'], d['amount']), reverse=True)
print (sr[:10])

# sortedamounts = sorted(amounts, key=lambda (a, r): a)
# print (sortedamounts)

# sortedresult = sorted(result, key=lambda d: (d['avgtimes']))
# displayResult(sortedresult)
