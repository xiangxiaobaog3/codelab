#!/usr/bin/env python
# encoding: utf-8

import random


def swap(array, i, j):
    print("swap", array, i, j)
    array[i], array[j] = array[j], array[i]


def qsort(array):
    if len(array) <= 1:
        return array

    pivot = array[0]
    less = []
    greater = []

    for x in array[1:]:
        if x < pivot:
            less.append(x)
        else:
            greater.append(x)

    print(less, pivot, greater)
    return qsort(less) + [pivot] + qsort(greater)


# def quick_sort(array, left, right):
#     if right > left:
#         q = partition(array, left, right)
#         # after partition
#         # -> A[left..q-1] <= A[q] <= A[q+1..right]
#         quick_sort(array, left, q-1)
#         quick_sort(array, q+1, right)


# def partition(array, left, right):
#     p = array[left]
#     i = left
#     j = right + 1


def bubble_sort(array):
    """依次比较相邻的数，如果大于/小于则交换位置，将最大/最小冒泡到最后一位"""
    print("--> bubble sort <--")
    for i, _ in enumerate(array):
        for j in range(0, len(array) - i-1):
            if array[j] < array[j+1]:
                swap(array, j, j+1)


def sort_1(array):
    for i, e1 in enumerate(array):
        for j in range(i+1, len(array)):
            if array[i] > array[j]:
                print('swap', i, j, e1, array[j])
                swap(array, i, j)




def main():
    li = [random.randint(0, 10) for i in range(10)]
    print(li)
    # bubble_sort(li)
    print(qsort(li), 'qsort')


if __name__ == '__main__':
    main()
