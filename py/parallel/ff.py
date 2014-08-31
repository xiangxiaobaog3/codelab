# encoding: utf-8

from multiprocessing import Pool
import time


def func(x):
    time.sleep(0.5)
    return [[len(z), z] for z in x]

if __name__ == '__main__':
    pool = Pool(processes=2)

    f = open('f.py', 'r')
    l = f.readlines()
    f.close()


    d = [w.strip() for w in l]

    result = pool.apply_async(func, args=[d])

    print result.get()
