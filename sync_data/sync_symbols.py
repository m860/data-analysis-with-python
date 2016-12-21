import requests
import random
import mysql.connector as connector
import json
import urllib
import os
import pandas as pd
from dateutil.parser import parse
import sys
import time
import numpy as np

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Cookie': 's=6y12o3weh9; xq_a_token=b4f6f5dfec2e69f2ede28dbae3756f62823c055b; xqat=b4f6f5dfec2e69f2ede28dbae3756f62823c055b; xq_r_token=98cdc852786ad0ad38f2f6713ec7106c1367f132; xq_is_login=1; u=4792737585; xq_token_expire=Fri%20Jan%2013%202017%2009%3A33%3A17%20GMT%2B0800%20(CST); bid=9ef535415d5813e413f9a5ee528789fd_iwveqn2s; Hm_lvt_1db88642e346389874251b5a1eded6e3=1481696993,1482111192; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1482111211'
}

symbols = np.array([])

symbolsPath = 'download/symbols.csv'


def getSymbols():
    global symbols
    with open(symbolsPath) as f:
        symbols = [i.replace('\n', '') for i in f.readlines()]


def saveBrokenPoint(page, pageSize):
    data = {
        'page': page,
        'pageSize': pageSize
    }
    dirname = 'temp'
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    filepath = '{}/sync_symbols.broken'.format(dirname)
    with open(filepath, 'w+') as f:
        json.dump(data, f)


def getBrokenPoint(filepath='temp/sync_symbols.broken'):
    if not os.path.exists(filepath):
        return None
    with open(filepath) as f:
        return json.load(f)


def removeBrokenPoint(filepath='temp/sync_symbols.broken'):
    if os.path.exists(filepath):
        os.remove(filepath)


def downloadPrice(symbol):
    dir = 'download'
    if not os.path.exists(dir):
        os.mkdir(dir)
    savepath = '{}/{}.csv'.format(dir, symbol)
    url = 'https://xueqiu.com/S/{}/historical.csv'.format(symbol)
    sys.stdout.write('download %s' % (url))
    res = requests.get(url, headers=HEADERS)
    if res.status_code == 200:
        # csv=pd.read_csv(res.con)
        with open(savepath, 'w+') as f:
            f.write(res.content)
    return savepath


def syncPrices():
    getSymbols()
    l = len(symbols)
    i = 1
    for s in symbols:
        sys.stdout.write('%s/%s ' % (i, l))
        downloadPrice(s)
        i += 1


def syncSymbols():
    global symbols, json
    page = 1
    pageSize = 30
    brokenPoint = getBrokenPoint()
    if not brokenPoint == None:
        page = int(brokenPoint['page'])
        pageSize = int(brokenPoint['pageSize'])
        removeBrokenPoint()

    url = "https://xueqiu.com/stock/cata/stocklist.json?page={}&size={}&order=desc&orderby=percent&type=11%2C12&_={}"
    while True:
        print("fetch page = %s" % page)
        try:
            res = requests.get(url.format(page, pageSize, random.random()), headers=HEADERS)
            if res.status_code == 200:
                json = res.json()
                stocklen = len(json['stocks'])
                if stocklen <= 0:
                    break
                symbols = np.append(symbols, [d['symbol'] for d in json['stocks']])
                page += 1
            else:
                saveBrokenPoint(page, pageSize)
                time.sleep(5)
                syncSymbols()

        except:
            print (sys.exc_info())
            saveBrokenPoint(page, pageSize)
            time.sleep(5)
            syncSymbols()
    with open(symbolsPath, 'w+') as f:
        f.write('\n'.join(symbols))


# syncSymbols()
# print(getSymbols())
syncPrices()
