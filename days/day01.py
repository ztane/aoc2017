from helpers import get_aoc_data

d = get_aoc_data(day=1)


def part1():
    the_sum = 0

    length = len(d.data)
    for i in range(length):
        if d.data[i] == d.data[(i + 1) % length]:
            the_sum += int(d.data[i])

    return the_sum


def part2():
    the_sum = 0
    length = len(d.data)
    for i in range(length):
        if d.data[i] == d.data[(i + length // 2) % length]:
            the_sum += int(d.data[i])

    return the_sum
