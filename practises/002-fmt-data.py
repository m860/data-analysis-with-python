from datetime import datetime
from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

with open('data/SZ#002637.txt', 'r') as f:
    lines = f.readlines()
    print len(lines)
    lines.pop(0)
    lines.pop(0)
    lines.pop(-1)
    print len(lines)
    fmtdata = [{'date': data[0], 'open': float(data[1]), 'high': float(data[2]), 'low': float(data[3]),
                'close': float(data[4])} for data in
               (i.replace('\t', ',').replace('\r\n', '').split(',') for i in lines)]
    print fmtdata
    frame = DataFrame(fmtdata)
    print frame['close'][:10]
    close_counter = frame['close'].value_counts();
    print close_counter[10:20]
    close_counter.plot(kind='barh', rot=0)
