from dateutil.parser import parse
from datetime import datetime


def getData():
    with open('data/SZ#002637.txt', 'r') as f:
        lines = f.readlines()
        print('total:{0}'.format(len(lines)))
        lines.pop(0)
        lines.pop(0)
        lines.pop(-1)
        return [{'date': parse(data[0]), 'open': float(data[1]), 'high': float(data[2]), 'low': float(data[3]),
                 'close': float(data[4])} for data in
                (i.replace('\t', ',').replace('\r\n', '').split(',') for i in lines)]
