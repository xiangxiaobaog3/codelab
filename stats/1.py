# encoding: utf-8

def mean(array):
    return (array * 1.0) / len(array)


def midrange(array):
    """
    中程数
    取最大数加最小数的平均值
    """
    array.sort()
    return (array[0] + array[-1]) / 2


def range_(array):
    """
    极差
    最大数与最小数的差值
    """
    array.sort()
    return array[-1] - array[0]



