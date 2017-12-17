from helpers import *

d = get_aoc_data(day=17)
skips = int(d.data)


def part1():
    spinlock = deque([0])

    for i in range(1, 2017 + 1):
        spinlock.rotate(-(skips + 1))
        spinlock.append(i)
        spinlock.rotate(1)

    print(spinlock[spinlock.index(2017) + 1])


def part2():
    spinlock = deque([0])

    for i in range(1, 50_000_000 + 1):
        spinlock.rotate(-(skips + 1))
        spinlock.append(i)
        spinlock.rotate(1)
        if i % 10000 == 0:
            print(i)

    print(spinlock[spinlock.index(0) + 1])
