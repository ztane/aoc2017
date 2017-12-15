from helpers import *

d = get_aoc_data(day=15)
mod = 2147483647
(_, a_start), (_, b_start) = d.parsed('Generator <> starts with <int>')
a_multiplier = 16807
b_multiplier = 48271


def part1():
    a = a_start
    b = b_start

    ct = 0
    for i in range(40_000_000):
        a *= a_multiplier
        a %= 2147483647
        b *= b_multiplier
        b %= 2147483647
        if a & 0xFFFF == b & 0xFFFF:
            ct += 1

    return ct


def part2():
    ct = 0

    def gen(v, m, multiple):
        while True:
            v *= m
            v %= 2147483647
            if v % multiple == 0:
                yield v

    g1 = gen(a_start, a_multiplier, 4)
    g2 = gen(b_start, b_multiplier, 8)

    for i in range(5_000_000):
        v1 = next(g1)
        v2 = next(g2)
        if v1 & 0xFFFF == v2 & 0xFFFF:
            ct += 1

    return ct
