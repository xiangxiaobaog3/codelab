from random import randrange

def shuffle(li):
    length = len(li)

    for i in range(1, length):
        j = randrange(0, i + 1)
        if j != i:
            li[i], li[j] = li[j], li[i]

    return li

print(shuffle(range(10)))
