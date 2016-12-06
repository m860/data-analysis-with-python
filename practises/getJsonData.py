from dateutil.parser import parse


def getJSONData(path='data/SZ#002637.txt'):
    with open(path, 'r') as f:
        lines = f.readlines()
        lines.pop(0)
        lines.pop(0)
        lines.pop(-1)
        return [{'date': parse(data[0]), 'open': float(data[1]), 'high': float(data[2]), 'low': float(data[3]),
                 'close': float(data[4]), 'volume': float(data[5]), 'volumeAmount': float(data[6])} for data in
                (i.replace('\t', ',').replace('\r\n', '').split(',') for i in lines)]


print (getJSONData())
