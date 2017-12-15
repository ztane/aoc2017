from functools import reduce
import operator as op

from helpers import get_aoc_data, ring_list

d = get_aoc_data(day=10)


def knot_it(knots, iterations=1):
    start = skip = 0
    state = ring_list(range(256))

    for _ in range(iterations):
        for span in knots:
            state[start: start + span] = state[start: start + span][::-1]
            start += skip + span
            skip += 1

    return state


def knot_hash(s):
    knots = list(s.encode()) + [17, 31, 73, 47, 23]
    h = knot_it(knots, iterations=64)
    return bytes(reduce(op.xor, h[i: i + 16]) for i in range(0, 256, 16))


def part1():
    knots = map(int, d.data.split(','))
    result = knot_it(knots, iterations=1)
    return result[0] * result[1]


def part2():
    return knot_hash(d.data).hex()
