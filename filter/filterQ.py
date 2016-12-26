from Stock import Stock
import numpy as np
import os

'''
states:
    close
    macd
    status:up,down,nochange
actions:
    in
    out
    none
rewards:
    0       nochange
    +50     up
    -100    down

'''

def getAllFiles(dirname="../sync_data/download"):
    files = None
    for dirpath, dirnames, filenames in os.walk(dirname):
        files = [os.path.join(dirpath, filename) for filename in filenames if
                 filename.startswith('SH') or filename.startswith("SZ")]
    return files


def getFile(symbol):
    files = getAllFiles()
    if not files == None:
        return [filename for filename in files if symbol in filename]
    return None


# print(getAllFiles())
print(getFile("002673"))