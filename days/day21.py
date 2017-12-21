import numpy
import numpy as np

from helpers import *

d = get_aoc_data(day=21)
rules = []


def parse_rule(line):
    return numpy.array([
        [cell == '#' for cell in row]
        for row in
        line.split('/')
    ])


@lru_cache(maxsize=None)
def find_rule(pattern):
    array = numpy.array(pattern)
    for ours in [array, array.T]:
        for flipped in [
            ours,
            numpy.flip(ours, 0),
            numpy.flip(ours, 1),
            numpy.flip(numpy.flip(ours, 0), 1)]:

            for src, tgt in rules:
                if numpy.array_equiv(flipped, src):
                    return tgt

    raise ValueError('No rule found')

def expand_map(the_map):
    rule_size, tgt_size = (2, 3) if len(the_map) % 2 == 0 else (3, 4)

    total = None
    for y in range(0, len(the_map), rule_size):
        row = None
        for x in range(0, len(the_map), rule_size):
            part = the_map[y: y + rule_size, x: x + rule_size]
            corresponding_rule = find_rule(tuple(map(tuple, part)))
            if row is None:
                row = corresponding_rule
            else:
                row = numpy.concatenate((row, corresponding_rule), axis=1)

        if total is None:
            total = row
        else:
            total = numpy.concatenate((total, row), axis=0)

    return total


def part1_and_2():
    global rules
    the_map = [[i == '#' for i in row] for row in """.#.\n..#\n###""".splitlines()]
    the_map = np.array(the_map)
    for src, tgt in d.parsed('<> => <>'):
        rules.append((parse_rule(src), parse_rule(tgt)))

    for i in range(18):
        if i == 5:
            part1 = numpy.count_nonzero(the_map)
        the_map = expand_map(the_map)

    return part1, numpy.count_nonzero(the_map)
