import math
import numpy

from helpers import get_aoc_data

d = get_aoc_data(day=12)


def part1_and_2():
    num_lines = len(d.lines)
    adj = numpy.zeros((num_lines, num_lines))

    for i in d.lines:
        n, m = i.split(' <-> ')
        to = map(int, m.split(', '))
        n = int(n)
        for i in to:
            adj[n][i] = adj[i][n] = 1
            print(n, i)

    for i in range(int(math.ceil(math.log2(n)))):
        print(1)
        adj = (adj @ adj) > 0

    multiplied = numpy.linalg.matrix_power(adj, 2000)
    n_in_group_0 = len(list(filter(bool, multiplied[0])))

    seen = set()
    groups = 0
    print(multiplied)
    for i in range(num_lines):
        if i not in seen:
            groups += 1
            for j in range(num_lines):
                if multiplied[i][j]:
                    seen.add(j)

    return n_in_group_0, groups
