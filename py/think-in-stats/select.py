def select(li):
    """select swap"""
    for idx, elem in enumerate(li):
        for jidx in range(idx+1, len(li)):
            if li[idx] > li[jidx]:
                t = li[idx]
                li[idx] = li[jidx]
                li[jidx] = t
                print('swap', idx, jidx)
    return li

li = range(20)
li.reverse()
li = [1, 3, 2, 6, 8, 10, 2, 3, 1, 3, 2, 12, 4, 1, 6, 2]
print(select(li))
