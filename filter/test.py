from Stock import Stock
import numpy as np

# print(type(np.zeros(5)))

stock = Stock('../sync_data/download/SH000027.csv')
print stock.datas
