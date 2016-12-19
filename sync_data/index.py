import requests
import random
import mysql.connector as connector
import json
import urllib
import os
import pandas as pd
from dateutil.parser import parse
import sys

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"

COOKIE = 's=6y12o3weh9; xq_a_token=b4f6f5dfec2e69f2ede28dbae3756f62823c055b; xqat=b4f6f5dfec2e69f2ede28dbae3756f62823c055b; xq_r_token=98cdc852786ad0ad38f2f6713ec7106c1367f132; xq_is_login=1; u=4792737585; xq_token_expire=Fri%20Jan%2013%202017%2009%3A33%3A17%20GMT%2B0800%20(CST); bid=9ef535415d5813e413f9a5ee528789fd_iwveqn2s; Hm_lvt_1db88642e346389874251b5a1eded6e3=1481696993,1482111192; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1482111211'


class Datetime64Converter(connector.conversion.MySQLConverter):
    """ A mysql.connector Converter that handles datetime64 types """

    def _timestamp_to_mysql(self, value):
        return value.view('<i8')


def getDbConfig():
    with open("dbconfig.json") as f:
        dbconfig = json.load(f)
        return dbconfig


def existedSymbol(symbol, connection):
    cursor = connection.cursor(buffered=True)
    cursor.execute('select * from tbl_Symbols where Symbol=\'%s\'', (symbol))
    l = cursor.rowcount
    cursor.close()
    return l > 0


def insertSymbol(symbol, exchangeCode, connection):
    cursor = connection.cursor()
    sql = 'insert into tbl_Symbols(Symbol,ExchangeCode) values(\'{}\',\'{}\')'.format(symbol, exchangeCode)
    cursor.execute(sql)
    connection.commit()
    cursor.close()


def insertPrices(symbol, prices):
    connection = connector.connect(**getDbConfig())
    # connection.set_converter_class(Datetime64Converter)
    cursor = connection.cursor()
    sql = "insert into tbl_Prices(Symbol,Date,Open,High,Low,Close,Volume) values(%s,%s,%s,%s,%s,%s,%s)"
    for p in prices:
        try:
            cursor.execute(sql, (symbol, p[1], p[2], p[3], p[4], p[5], p[6]))
        except:
            print(p)
            raise
    connection.commit()
    cursor.close()
    connection.close()


def getLatestPrice(symbol):
    connection = connector.connect(**getDbConfig())
    cursor = connection.cursor()
    cursor.execute('select * from tbl_Prices where Symbol=\'{}\' order by Date desc limit 1'.format(symbol))
    price = cursor.fetchone()
    cursor.close()
    connection.close()
    return price


def splitCode(code):
    return (code[:2], code[2:])


def batchUpdateCodes(codes):
    connection = connector.connect(**getDbConfig())
    for code in codes:
        exchangeCode, symbol = splitCode(code)
        if existedSymbol(symbol, connection):
            continue
        else:
            insertSymbol(symbol, exchangeCode, connection)
    connection.close()


def syncCodes():
    headers = {
        "User-Agent": USER_AGENT,
        "Cookie": COOKIE
    }
    page = 1
    url = "https://xueqiu.com/stock/cata/stocklist.json?page={}&size=30&order=desc&orderby=percent&type=11%2C12&_={}"
    while True:
        print("fetch page = %s" % page)
        res = requests.get(url.format(page, random.random()), headers=headers)
        if res.status_code == 200:
            json = res.json()
            stocklen = len(json['stocks'])
            if stocklen <= 0:
                break
            # update codes
            batchUpdateCodes([d['symbol'] for d in json['stocks']])
            page += 1
        else:
            raise res.status_code


def getSymbols():
    connection = connector.connect(**getDbConfig())
    cursor = connection.cursor(buffered=True)
    cursor.execute('select Symbol,ExchangeCode,SysNo from tbl_Symbols')
    symbols = cursor.fetchall()
    cursor.close()
    return symbols


def downloadPrice(symbol):
    dir = 'download'
    if not os.path.exists(dir):
        os.mkdir(dir)
    savepath = '{}/{}.csv'.format(dir, symbol)
    url = 'https://xueqiu.com/S/{}/historical.csv'.format(symbol)
    print('download {}'.format(url))
    res = requests.get(url, headers={
        "User-Agent": USER_AGENT,
        'Cookie': COOKIE
    })
    if res.status_code == 200:
        # csv=pd.read_csv(res.con)
        with open(savepath, 'w+') as f:
            f.write(res.content)
    return savepath


def saveBreakPoint(sysNo, type='price'):
    dir = 'temp'
    if not os.path.exists(dir):
        os.mkdir(dir)
    filepath = '{}/{}.break'.format(dir, type)
    with open(filepath, 'a') as f:
        f.write(sysNo)


def getBreakPoint(type='price'):
    filepath = 'temp/{}.break'.format(type)
    if os.path.exists(filepath):
        with open(filepath) as f:
            return f.readline()
    else:
        return None


def syncPrices():
    symbols = getSymbols()
    bp = getBreakPoint()
    if not bp == None:
        symbols = [(a, b, c) for a, b, c in symbols if c >= int(bp)]

    slen = len(symbols)
    i = 1

    for symbol, ecode, sysno in symbols:
        try:
            sys.stdout.write('%s/%s ' % (i, slen))
            filepath = downloadPrice(ecode + symbol)
            csv = pd.read_csv(filepath)
            if csv.size > 0:
                latestPrice = getLatestPrice(symbol)
                if latestPrice == None:
                    print("[{}] full import . total = {}".format(symbol, len(csv.index)))
                    insertPrices(symbol, csv.values)
                else:
                    diff = [d for d in csv.values if parse(d[1]).date() > latestPrice[8]]
                    print("[{}] delta import . total = {}".format(symbol, len(diff)))
                    insertPrices(symbol, diff)
            i += 1
        except:
            saveBreakPoint(sysno)
            raise


# syncCodes()

syncPrices()
