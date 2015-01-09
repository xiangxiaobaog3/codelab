# encoding: utf-8

from random import randint

from qsort import qsort_inplace, qsort_1

def swap(array, i, j):
    t = array[j]
    array[j] = array[i]
    array[i] = t


def bubble_sort(array):

    length = len(array)

    for i in range(length):
        for j in range(i+1, length):
            if array[i] > array[j]:
                swap(array, i, j)

    return array


def insertion_sort(array):
    for i in range(1, len(array)):
        t = array[i]
        j = i - 1
        while j >= 0 and t > array[j]:
            array[j+1] = array[j]
            j -= 1
        array[j+1] = t;


def generate_random_array():
    return [randint(1, 20) for i in range(10)]


def main():
    array = generate_random_array()
    print("To be sort %s" % array)
    # print(bubble_sort(array))
    qsort_1(array, 0, len(array)-1)
    print(array)


if __name__ == '__main__':
    main()
