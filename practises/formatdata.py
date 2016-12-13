# -*- coding: UTF-8 -*-

from classes import Stock, format
import numpy as np
import os


def getFiles(dirname):
    files = []
    for dirpath, dirnames, filenames in os.walk(dirname):
        files.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.txt')])
    return files


def getName(filepath):
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    return name


files = getFiles('original')
for p in files:
    print('formating {0}'.format(p))
    format(p, os.path.join('formated', getName(p) + '.json'))
