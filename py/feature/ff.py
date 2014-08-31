#-*- encoding:utf-8 -*-
import os

def get_files(files, limit=5):
    n = 0
    fl = []
    for fn in files:
        if n == limit:
            n = 0
            yield fn
            fl = []
        else:
            fl.append(fn)
            n += 1

for fs in get_files(os.listdir('.'), 2):
    print fs
