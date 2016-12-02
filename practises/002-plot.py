import matplotlib.pyplot as plt
from helper import getData

fmtdata = getData()
line = plt.plot([data['date'] for data in fmtdata], [data['close'] for data in fmtdata])
plt.ylabel = 'close'
plt.xlabel = 'date'
plt.show()
