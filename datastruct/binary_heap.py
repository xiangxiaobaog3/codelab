#!/usr/bin/env python
# encoding: utf-8
import random

'''
heap order property ias as follows: in a heap, for every node `x` with parent `p`, the key in `p` is smaller than
or equal to the key in `x`

'''
class BinaryHeap(object):
    def __init__(self):
        self.heap_list = [0]
        self.current_size = 0

    def get_parent(self, index):
        # 索引除2
        return index / 2

    def swap(self, k, j):
        t = k
        k = j
        j = t

    def percolate_up(self, i):
        while self.get_parent(i) > 0:
            value = self.heap_list[i]
            pvalue = self.heap_list[self.get_parent(i)]
            if pvalue > value:
                self.heap_list[i] = pvalue
                self.heap_list[self.get_parent(i)] = value
            i = self.get_parent(i)

    def insert(self, k):
        self.heap_list.append(k)
        self.current_size += 1
        self.percolate_up(self.current_size)

    def min_child(self, i):
        if i * 2 + 1 > self.current_size:
            return i * 2
        else:
            if self.heap_list[i*2] < self.heap_list[i*2 + 1]:
                return i * 2
            else:
                return i * 2 + 1

    def percolate_down(self, i):
        while (i*2) <= self.current_size:
            mc = self.min_child(i)
            if self.heap_list[i] > self.heap_list[mc]:
                tmp = self.heap_list[i]
                self.heap_list[i] = self.heap_list[mc]
                self.heap_list[mc] = tmp
            i = mc

    def del_min(self):
        retval = self.heap_list[1]
        self.heap_list[1] = self.heap_list.pop()
        self.current_size -= 1
        self.percolate_down(1)
        return retval

    def build_heap(self, alist):
        i = len(alist) / 2
        self.current_size = len(alist)
        self.heap_list = [0] + alist[:]

        while (i > 0):
            self.percolate_down(i)
            i = i - 1


b = BinaryHeap()
b.insert(10)
b.insert(9)
b.insert(7)
b.insert(3)
b.insert(5)
b.insert(10)
print(b.heap_list)
b.del_min()
print(b.heap_list)
b.del_min()
print(b.heap_list)
b.del_min()
print(b.heap_list)

b.build_heap([random.randint(1, 100) for i in range(10)])
print('---')
print(b.heap_list)
b.del_min()
print(b.heap_list)
