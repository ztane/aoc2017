import math
from collections import defaultdict

import numpy

from helpers import get_aoc_data

d = get_aoc_data(day=12)


def part1_and_2():
    num_lines = len(d.lines)
    adj = numpy.zeros((num_lines, num_lines))

    for n, m in d.parsed('<> <<-> <str:.*>'):
        to = map(int, m.split(', '))
        n = int(n)
        for line in to:
            adj[n][line] = adj[line][n] = 1

    old = adj
    ct = 0
    while adj.all() == old.all():
        print(ct)
        old = adj
        adj = (adj @ adj) > 0

    n_in_group_0 = len(list(filter(bool, adj[0])))
    seen = set()
    groups = 0
    for line in range(num_lines):
        if line not in seen:
            groups += 1
            for j in range(num_lines):
                if adj[line][j]:
                    seen.add(j)

    return n_in_group_0, groups
