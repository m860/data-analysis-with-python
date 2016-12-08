# -*- coding: UTF-8 -*-
import numpy as np


# 均线
def ma(ndarr, num=5):
    if not isinstance(ndarr, np.ndarray):
        raise 'parameter ndarr is not a np.ndarray'
    return np.append(np.zeros(num),
                     [ndarr[index - num:index].mean(dtype=np.float64) for index in np.arange(num, ndarr.size)])


# 指数平均数
# 一般num取12 or 26
def ema(ndarr, num=12):
    a = 2 / (num + 1)

    def curema(arr):
        if len(arr) == 1:
            return arr[0]
        return a * arr[-1] + (1 - a) * curema(arr[:-1])

    return np.append(np.zeros(12, dtype=np.float64), [curema(ndarr[:i]) for i in np.arange(num, ndarr.size)])


# 指数平滑移动平均线
def macd(ndarr, num=12):
    emas = ema(ndarr, num)
    return np.append(np.zeros(num + 1), [emas[i - 1] * (num - 1) / (num + 1) + ndarr[i] * 2 / (num + 1) for i in
                                         np.arange(num + 1, ndarr.size)])


# 波峰/波谷
def getPeackAndTrough(values):
    def calTrend(value):
        if value > 0:
            return 1
        elif value < 0:
            return -1
        else:
            return 0

    def calDiffR(value1, value2):
        if value1 == 0 and value2 >= 0:
            return 1
        elif value1 == 0 and value2 < 0:
            return -1
        else:
            return value1

    def findPeackValue(value, index):
        if value == 2:
            return ('speack', value)
        else:
            return ('trough', value)

    diffv = [values[i + 1] - values[i] for i in range(len(values)) if i < len(values) - 1];
    trend = [calTrend(v) for v in diffv]
    r = [calDiffR(trend[i], trend[i + 1]) for i in range(len(trend) - 1)]
    diffr = [r[i + 1] - r[i] for i in range(len(r)) if i < len(r) - 1]
    values = [i + 1 for i in range(len(diffr)) if diffr[i] == 2 or diffr[i] == -2]
    return values
