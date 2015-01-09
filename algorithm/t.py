#!/usr/bin/env python
# encoding: utf-8


a = [0 for i in range(11)]

li = [3, 2, 5, 5, 8]

for i in li:
    a[i] += 1

for i, e in enumerate(a):
    if e == 0:
        continue
    print(' '.join(str(i) * e))
