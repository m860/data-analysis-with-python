# from multiprocessing.dummy import Pool as ThreadPool

# def squareNumber(n):
#     print(n)
#     return n ** 2
#
#
# # function to be mapped over
# def calculateParallel(numbers, threads=2):
#     pool = ThreadPool(threads)
#     results = pool.map(squareNumber, numbers)
#     pool.close()
#     pool.join()
#     return results
#
#
# numbers = [1, 2, 3, 4, 5]
# squaredNumbers = calculateParallel(numbers, 4)
# for n in squaredNumbers:
#     print(n)

from multiprocessing import Pool
# from multiprocessing.dummy import Pool
import numpy as np

def add(x, y):
    return x + y


def addWrapper(args):
    return add(*args)

def cb(r):
    print(r)

num1 = range(10)
num2 = range(5)

pool = Pool(2)
result = pool.map_async(addWrapper, zip(num1,num2),callback=cb)
# result = pool.starmap(add, zip(num1, num2))
pool.close()
print(result)
# print(zip(num1,num2))
print (np.full(5,1))

