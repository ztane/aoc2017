from collections import defaultdict

from helpers import get_aoc_data, spiral_walk, cmanhattan, cneighbours_8

d = get_aoc_data(day=3)


def part1():
    for n, coords in enumerate(spiral_walk(), 1):
        if n == d.as_int:
            return cmanhattan(coords)


def part2():
    target = d.as_int
    values = defaultdict(int, {0: 1})

    for i in spiral_walk():
        values[i] = sum(values[c] for c in cneighbours_8(i, add_self=True))
        if values[i] > target:
            return values[i]
