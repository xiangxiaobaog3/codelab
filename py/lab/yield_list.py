#-*- encoding:utf-8 -*-

li = range(100)
step = 100
def _range(li, step):
    start = 0
    stop = len(li)
    li = range(start, stop, step)
    if li[-1] != stop:
        li.append(stop)
    return li

#_li = _range(li, step)
#for e in _li:
    #start = e
    #_index = _li.index(e)
    #if _li.index(e) != len(_li) - 1:
        #stop = _li[_li.index(e) + 1]
        #print  li[start:stop]


def limit_output(step):
    start = 0
    def _range(li):
        stop = len(li)
        _li = range(start, stop, step)
        if _li[-1] != stop:
            _li.append(stop)
        _li_length = len(_li)
        for el in _li:
            _el_index = _li.index(el)
            if _el_index != _li_length - 1:
                bottom = _li[_el_index + 1]
                yield li[el:bottom]
    return _range

for i in limit_output(3)(li):
    print i
