# -*- coding: UTF-8 -*-

import stock as helper
import numpy as np
import matplotlib.pyplot as plt


# dataPath = 'data/SZ#002637.txt'
#
#
# def case1(path):
#     lines = None
#     with open(path) as f:
#         lines = f.readlines()
#         lines.pop(0)
#         lines.pop(0)
#         lines.pop(-1)
#     closes = [np.float64(c[4]) for c in (r.replace('\t', ',').replace('\r\n', '').split(',') for r in lines)]
#     dates = [c[0] for c in (r.replace('\t', ',').replace('\r\n', '').split(',') for r in lines)]
#     macd, diff, dea = stock.macd(np.array(closes))
#
#     # def findExtrema(diff, dea):
#     #     def trend(value):
#     #         if value > 0:
#     #             return 1
#     #         elif value < 0:
#     #             return -1
#     #         else:
#     #             return 0
#     #
#     #     values = [trend(v) for v in diff - dea]
#     #     values2 = [values[i + 1] - values[i] for i in np.arange(len(values) - 1)]
#     #
#     #     return [(i+1,diff[i+1],dea[i+1]) for i in np.arange(len(values2)) if values2[i] == 2 or values2[i] == -2]
#     #
#     # # 计算diff和dea的相交后的第一个点
#     # extremas = findExtrema(diff, dea)
#     # print ([dates[i] for i,diffv,deav in extremas])
#
#     # 计算macd的转折点,此点是转折后的第一个点
#     def findFirstTurningFromMACD(macd):
#         return [(i + 1,macd[i+1]) for i in np.arange(macd.size - 1) if
#                 (macd[i + 1] > 0 and macd[i] <= 0) or (macd[i + 1] < 0 and macd[i] >= 0)]
#
#     print([(dates[index],value,closes[index]) for index,value in findFirstTurningFromMACD(macd)])
#
#
# case1(dataPath)

class StockCase:
    property = 100000
    repository = 0
    fee = 0

    def buy(self, price):
        StockCase.repository = int(StockCase.property / price)
        amount = StockCase.repository * price
        StockCase.property -= amount
        StockCase.fee += helper.fee(amount)
        print('In --> repository:{0},property:{1},fee:{2},buy price:{3}'.format(StockCase.repository,
                                                                                StockCase.property, StockCase.fee,
                                                                                price))

    def sale(self, price):
        amount = StockCase.repository * price
        StockCase.repository = 0
        StockCase.fee += helper.fee(amount, type=1)
        StockCase.property += amount
        print('Out --> repository:{0},property:{1},fee:{2},sale price:{3}'.format(StockCase.repository,
                                                                                  StockCase.property, StockCase.fee,
                                                                                  price))

    def display(self):
        print(
            'property:{0},fee:{1},repository:{2},balance:{3}'.format(StockCase.property, StockCase.fee,
                                                                     StockCase.repository,
                                                                     StockCase.property - StockCase.fee))


class Stock:
    def __init__(self, data):
        if not isinstance(data, np.ndarray):
            raise 'data must be np.array'
        self.data = data
        self.macd, self.diff, self.dea = helper.macd(np.array([d['close'] for d in self.data]))

    def findFirstTurningFromMACD(self):
        return [(i + 1, self.macd[i + 1]) for i in np.arange(self.macd.size - 1) if
                (self.macd[i + 1] > 0 and self.macd[i] <= 0) or (self.macd[i + 1] < 0 and self.macd[i] >= 0)]


class TestCase(StockCase):
    def run(self, stock):
        if not isinstance(stock, Stock):
            raise 'stock must be Stock'
        self.stock = stock
        buyPosition = [i for i, macd in self.stock.findFirstTurningFromMACD() if macd > 0]
        # print([self.stock.data[i]['date'] for i, macd in buyPosition if macd > 0])
        dk = helper.diffk(stock.diff)
        salePosition = helper.findSalePosition(stock.diff)
        # print([(stock.data[k]['date'],dk[k-1],dk[k]) for k,v in salePosition])
        # print (dk)
        for i in buyPosition:
            buyPrice = stock.data[i]['close']
            print(stock.data[i]['date'])
            self.buy(buyPrice)
            salePriceIndexes = [j for j, v in salePosition if j > i]
            if len(salePriceIndexes) > 0:
                salePriceIndex = salePriceIndexes[0]
                salePrice = stock.data[salePriceIndex]['close']
                print(stock.data[salePriceIndex]['date'])
                self.sale(salePrice)
                # self.display()
        self.display()
        print('last price:{0},amount:{1}'.format(stock.data[-1]['close'],stock.data[-1]['close']*StockCase.repository))


dataPath = 'data/SZ#002637.txt'


def getJSONData(path='data/SZ#002637.txt'):
    with open(path, 'r') as f:
        lines = f.readlines()
        lines.pop(0)
        lines.pop(0)
        lines.pop(-1)
        return np.array([{'date': data[0], 'open': float(data[1]), 'high': float(data[2]), 'low': float(data[3]),
                          'close': np.float64(data[4]), 'volume': float(data[5]), 'volumeAmount': float(data[6])} for
                         data in
                         (i.replace('\t', ',').replace('\r\n', '').split(',') for i in lines)])


# closes = np.array([d['close'] for d in getJSONData()])

case = TestCase()
case.run(Stock(getJSONData()))
