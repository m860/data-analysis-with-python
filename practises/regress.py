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

def run():
    rate = 0.03
    dateRange = np.arange(date(2016, 1, 1), date(2016, 12, 12)).astype(date)
    files = getFiles()
    for dt in dateRange[:50]:
        turnings = np.array([])
        for fp in files[:2]:
            stock = Stock()
            stock.load(fp)
            r5 = findLatestRecords(stock, dt)
            r5len = len(r5)
            if r5len >= 2:
                last = r5[-1]
                if not last['odate'] == dt:
                    break
                isTurning = stock.isFirstTurningByMACD(last, r5[-2])
                if isTurning:
                    turnings = np.append(turnings,[last])

        print turnings


run()
