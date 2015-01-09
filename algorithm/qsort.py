#!/usr/bin/env python
# encoding: utf-8

"""
Divde And Conque
"""

def swap(array, i, j):
    print('swap', array, i, j)
    array[i], array[j] = array[j], array[i]

def qsort(array):
    """
    缺点是需要额外的存储空间，也会影响速度和cache
    """
    if len(array) <= 1:
        return array

    pivot = array[0]
    less = [x for x in array[1:] if x < pivot]
    greater = [x for x in array[1:] if x >= pivot]

    return qsort(less) + [pivot] + qsort[greater]


def partition(array, left, right, pivot_idx):
    pivot = array[pivot_idx]
    swap(array, pivot_idx, right) # 把 pivot 移到末尾
    store_idx = left
    for i in range(left, right-1):
        if array[i] < pivot:
            swap(array, store_idx, i)
            store_idx += 1
    swap(array, right, store_idx)
    return store_idx

def qsort_inplace(array):
    if len(array) <= 1:
        return array
    idx = partition(array, 0, len(array)-1, 0)
    return qsort_inplace(array[:idx]) + qsort_inplace(array[idx+1:])


def qsort_1(array, left, right):
    if left > right:
        return
    pivot = array[left]
    i = left
    j = right

    while (i != j):

        # 先往右边找
        while (array[j] >= pivot and i < j):
            j -= 1

        # 再从左边找
        while (array[i] <= pivot and i < j):
            i += 1

        if (i < j):
            print('swap', i, j, array)
            array[i], array[j] = array[j], array[i]

    array[left], array[i] = array[i], array[left]
    qsort_1(array, left, i-1)
    qsort_1(array, i+1, right)
