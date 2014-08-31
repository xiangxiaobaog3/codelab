def quick_sort(array):
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            else:
                greater.append(x)
        return quick_sort(less) + equal + quick_sort(greater)
    return array

print quick_sort([1, 3, 2, 5, 8, 10, 2, 1, 3, 4, 7])
