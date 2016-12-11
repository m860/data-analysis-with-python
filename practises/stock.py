# -*- coding: UTF-8 -*-
import numpy as np


# 均线
def ma(ndarr, num=5):
    if not isinstance(ndarr, np.ndarray):
        raise 'parameter ndarr is not a np.ndarray'
    return np.append(np.zeros(num),
                     [ndarr[index - num + 1:index + 1].mean(dtype=np.float64) for index in np.arange(num, ndarr.size)])


# 指数平均数
# 一般num取12 or 26
# a=2/(N+1) N:周期天数
# EMA(t)=EAM(t-1)+a*(CLOSE(t)-EMA(t-1))
def ema(ndarr, cycle=12):
    a = 2 / np.float64((cycle + 1))
    ema0 = ndarr[0]
    result = np.array([ema0])

    def curema(index, value):
        return result[index - 1] + a * (value - result[index - 1])

    for i in np.arange(1, ndarr.size):
        result = np.append(result, [curema(i, ndarr[i])])

    return result


# 指数平滑移动平均线
def macd(ndarr):
    ema12 = ema(ndarr, 12)
    ema26 = ema(ndarr, 26)
    diff = ema12 - ema26
    dea = ema(diff, 9)
    osc = diff - dea
    return (osc * 2, diff, dea)


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
