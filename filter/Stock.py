# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
import os
from dateutil.parser import parse


def _macd(closes):
    ema12 = _ema(closes, 12)
    ema26 = _ema(closes, 26)
    diff = ema12 - ema26
    dea = _ema(diff, 9)
    osc = diff - dea
    return (osc * 2, diff, dea)


def _ma(closes, cycle=5):
    result = np.zeros(cycle)
    for i in np.arange(cycle, closes.size):
        result = np.append(result, [np.mean(closes[i - cycle:i])])
    return result


def _ema(closes, cycle=12):
    if closes.size <= 0:
        return np.array([])
    a = 2 / np.float64((cycle + 1))
    ema0 = closes[0]
    result = np.array([ema0])

    def curema(index, value):
        return result[index - 1] + a * (value - result[index - 1])

    for i in np.arange(1, closes.size):
        result = np.append(result, [curema(i, closes[i])])

    return result


def splicsvpath(csvpath):
    bn = os.path.basename(csvpath)
    filename, ext = os.path.splitext(bn)
    return (filename[2:], filename[:2])


class Stock:
    def __init__(self, csvpath, cal=True):
        self.symbol, self.code = splicsvpath(csvpath)
        self.datas = [{
                          'date': parse(d[1]).date(),
                          'open': np.float64(d[2]),
                          'high': np.float64(d[3]),
                          'low': np.float64(d[4]),
                          'close': np.float64(d[5]),
                          'volume': np.float64(d[6])
                      } for d in pd.read_csv(csvpath).as_matrix()]
        if cal:
            closes = np.array([d['close'] for d in self.datas])
            self.macd, self.div, self.dea = _macd(closes)
            self.em5 = _ma(closes, 5)
            self.em10 = _ma(closes, 10)
            self.em20 = _ma(closes, 20)
            self.em30 = _ma(closes, 30)
            self.em60 = _ma(closes, 60)
            self.ema5 = _ema(closes, 5)
            self.ema10 = _ema(closes, 10)
            self.ema20 = _ema(closes, 20)
            self.ema60 = _ema(closes, 60)

    def length(self):
        return len(self.datas)
