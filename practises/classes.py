# -*- coding: UTF-8 -*-
import numpy as np
import json
import os


def macd(ndarr):
    ema12 = ema(ndarr, 12)
    ema26 = ema(ndarr, 26)
    diff = ema12 - ema26
    dea = ema(diff, 9)
    osc = diff - dea
    return (osc * 2, diff, dea)


def format(fpath, tpath):
    items = None
    with open(fpath, 'r') as f:
        lines = f.readlines()
        lines.pop(0)
        lines.pop(0)
        lines.pop(-1)
        items = [{
                     'date': data[0],
                     'open': np.float64(data[1]),
                     'high': np.float64(data[2]),
                     'low': np.float64(data[3]),
                     'close': np.float64(data[4]),
                     'volume': np.float64(data[5]),
                     'amount': np.float64(data[6])
                 }
                 for data in (i.replace('\t', ',').replace('\r\n', '').split(',') for i in lines)]

    l = len(items)
    closes = np.array([d['close'] for d in items])

    # cal ema
    ema5 = ema(closes, 5)
    ema10 = ema(closes, 10)
    ema20 = ema(closes, 20)
    ema60 = ema(closes, 60)
    # cal macd
    _macd, diff, dea = macd(closes)
    diffv = [diff[i] - diff[i - 1] for i in range(diff.size) if i > 0]
    diffv.insert(0, 0)
    # cal mean
    for i in range(l):
        if i < 5:
            items[i]['ma5'] = 0
        else:
            items[i]['ma5'] = np.mean(closes[i - 5:i])
        if i < 10:
            items[i]['ma10'] = 0
        else:
            items[i]['ma10'] = np.mean(closes[i - 10:i])
        if i < 20:
            items[i]['ma20'] = 0
        else:
            items[i]['ma20'] = np.mean(closes[i - 20:i])
        if i < 30:
            items[i]['ma30'] = 0
        else:
            items[i]['ma30'] = np.mean(closes[i - 30:i])
        if i < 60:
            items[i]['ma60'] = 0
        else:
            items[i]['ma60'] = np.mean(closes[i - 60:i])
        items[i]['ema5'] = ema5[i]
        items[i]['ema10'] = ema10[i]
        items[i]['ema20'] = ema20[i]
        items[i]['ema60'] = ema60[i]
        items[i]['macd'] = _macd[i]
        items[i]['diff'] = diff[i]
        items[i]['dea'] = dea[i]
        items[i]['diffv'] = diffv[i]

    with open(tpath, 'w+') as f:
        json.dump(items, f)


def ema(ndarr, cycle=12):
    if ndarr.size <= 0:
        return np.array([])
    a = 2 / np.float64((cycle + 1))
    ema0 = ndarr[0]
    result = np.array([ema0])

    def curema(index, value):
        return result[index - 1] + a * (value - result[index - 1])

    for i in np.arange(1, ndarr.size):
        result = np.append(result, [curema(i, ndarr[i])])

    return result


class Stock:
    def _determineItems(self):
        if not self.items:
            raise 'you must load some data'

    def getCode(self, path):
        basename = os.path.basename(path)
        filename, ext = os.path.splitext(basename)
        return filename.split('#')[1]

    def load(self, path):
        self.path = path
        self.code = self.getCode(path)
        with open(path, 'r') as f:
            self.items = json.load(f)
        pass

    def save(self):
        with open(self.path, 'w+') as f:
            json.dump(self.items, f)

    def findBuyPosition(self):
        self._determineItems()
        return [self.items[i + 1] for i in range(len(self.items) - 1)
                if self.items[i + 1]['macd'] >= 0 and self.items[i]['macd'] < 0]

    def canBeEnter(self):
        if len(self.items) <= 0:
            return False
        lastest = self.items[-1]
        # macd>0 说明是多头
        # diffv>0 说明还在上升期
        # volume>0 说明没有停牌
        if lastest['macd'] >= 0 and lastest['diffv'] >= 0 and lastest['volume'] > 0:
            return True
        return False

    def isFirstTurningByMACD(self):
        l = len(self.items)
        if l < 2:
            return False
        if self.items[-2]['macd'] <= 0 and self.items[-1]['macd'] > 0 and self.items[-1]['volume'] > 0:
            return True
        return False

    def blocked(self):
        l = len(self.items)
        if l < 2:
            return True
        if self.items[-1]['close'] == self.items[-1]['open']:
            return True
        return False

    def addPrice(self, data):
        self._determineItems()
        # TODO check date
