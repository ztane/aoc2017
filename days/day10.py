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


def part1():
    knots = map(int, d.data.split(','))
    result = knot_it(knots, iterations=1)
    return result[0] * result[1]


def part2():
    knots = list(d.data.encode()) + [17, 31, 73, 47, 23]
    result = knot_it(knots, iterations=64)

    hash_value = ''.join(
        f'{reduce(op.xor, result[i: i + 16]):02x}' for i in range(0, 256, 16)
    )
    return hash_value