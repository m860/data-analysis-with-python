import matplotlib.pyplot as plt
from helper import getData, getPeackAndTrough

# fmtdata = getData()
# getPeackAndTrough([data['close'] for data in fmtdata])

# testData = [-5, 10, 10, 14, 14, 8, 8, 6, 6, -3, 2, 2, 2, 2, -3]
testData = [data['close'] for data in getData()[:10]]
print(testData)
indexs = getPeackAndTrough(testData)
values = [testData[i] for i in indexs]
print(values)

line1 = plt.plot(range(len(testData)), testData)
line2 = plt.plot(indexs, values,'r-')
plt.show()
