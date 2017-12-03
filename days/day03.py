from helpers import *

d = get_aoc_data(day=3)


def part1():
    for n, coords in enumerate(spiral_walk(), 1):
        if n == int(d.data):
            return cmanhattan(coords)


def part2():
    vals = {(0 + 0j): 1}
    target = int(d.data)

    def neighbour_sum(coords):
        the_sum = 0
        for i in [1, -1, 1j, -1j, 1 + 1j, 1 - 1j, -1 + 1j, -1 - 1j]:
            the_sum += vals.get(coords + i, 0)

        return the_sum

    for i in spiral_walk():
        if i == 0:
            continue

        the_value = neighbour_sum(i)
        if the_value > target:
            return the_value

        vals[i] = the_value
