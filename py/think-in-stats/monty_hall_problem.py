#!/usr/bin/env python
# encoding: utf-8

import random


def monty_hall_problem(counts):
    success = 0

    for i in xrange(counts):
        # generate three doors
        doors = [0 for i in range(3)]
        k = random.randint(0, len(doors) - 1)
        doors[k] = 1 # which has car
        p = random.randint(0, len(doors) - 1) # pick a door

        # pop a door
        doors.pop(p)
        if random.choice(doors) == 1:
            success += 1

    print(success * 1.0 / counts)

def main():
    monty_hall_problem(100000)

if __name__ == '__main__':
    main()
