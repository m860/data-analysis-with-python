# -*- coding: UTF-8 -*-

from classes import Stock, format, ThreadFormatStock
import numpy as np
import os
import sys
import Queue


def getFiles(dirname):
    files = []
    for dirpath, dirnames, filenames in os.walk(dirname):
        files.extend([os.path.join(dirpath, f) for f in filenames if f.endswith('.txt')])
    return files


def getName(filepath):
    basename = os.path.basename(filepath)
    name, ext = os.path.splitext(basename)
    return name


def formatProxy((filepath, jsonpath, index)):
    print('%s formating %s' % (index, filepath))
    format(filepath, jsonpath)


def callback():
    print('callback')


def buildFilepath(filepath, index, l):
    return (filepath, os.path.join('formated', getName(filepath) + '.json'), index, l);


def run_async(threads=10):
    files = getFiles('original')
    queue = Queue.Queue()
    l = len(files)
    for i in range(threads):
        f = ThreadFormatStock(queue)
        f.setDaemon(True)
        f.start()

    for arg in [buildFilepath(files[i], i, l) for i in range(l)]:
        queue.put(arg)

    queue.join()

def run():
    files = getFiles('original')
    l = len(files)
    i = 0
    for p in files:
        print('{1}/{2} formating {0}'.format(p, i, l))
        format(p, os.path.join('formated', getName(p) + '.json'))
        i += 1

run()
# format('original/SZ#002673.txt','formated/SZ#002673.json')
# run_async()