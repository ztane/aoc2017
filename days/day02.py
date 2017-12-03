from itertools import permutations

from helpers import get_aoc_data

d = get_aoc_data(day=2)


def part1():
    return sum(max(row) - min(row) for row in d.integer_matrix)


def part2():
    the_sum = 0
    for row in d.integer_matrix:
        for i1, i2 in permutations(row, 2):
            if not i2 % i1:
                the_sum += i2 // i1
                break

    return the_sum
