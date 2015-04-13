#!/usr/bin/env python
# encoding: utf-8

import math

FLAG_FIRST = 0
FLAG_LAST = 1


def binary_search(array, el, flag=FLAG_FIRST):
    first = 0
    last = len(array) - 1

    while first <= last:
        midpoint = (first + last) / 2
        mv = array[midpoint]
        if mv > el:
            last = midpoint
        elif mv < el:
            first = midpoint
        else:
            if flag == FLAG_FIRST and array[midpoint-1] == el:
                # search between first-mid
                f, l = first, midpoint
                while f <= l:
                    t = int(math.floor((f + l) / 2)) # 向下取整
                    print("search between first-mid", t, f, l)
                    if array[t] == el:
                        if t == 0 or array[t-1] != el:
                            return t
                        l = t
                    elif array[t] < el:
                        f = t
            elif (flag == FLAG_LAST and array[midpoint+1] == el):
                # search between mid-last
                f, l = midpoint, last
                while f <= l:
                    t = f + int(math.ceil((l - f) / 2.0)) # 向上取整
                    print("search between mid-last", t, f, l)
                    if array[t] == el:
                        if t == last or array[t+1] != el:
                            return t
                        f = t
                    elif array[t] > el:
                        l = t
    return midpoint

array = [2 for i in range(4000)]
array = [1, 2,2,2,2,2,2,2,2,2, 5]
idx = binary_search(array, 2, FLAG_FIRST)
print(idx, array[idx] == 2, idx==1)

idx = binary_search(array, 2, FLAG_LAST)
print(idx, array[idx] == 2, idx==len(array) - 2)
