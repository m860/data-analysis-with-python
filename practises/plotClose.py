import matplotlib.pyplot as plt
from getJsonData import getJSONData

fmtdata = getJSONData()
line = plt.plot([data['date'] for data in fmtdata], [data['close'] for data in fmtdata])
plt.ylabel = 'close'
plt.xlabel = 'date'
plt.show()
