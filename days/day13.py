from itertools import count

from helpers import get_aoc_data, defaultdict

d = get_aoc_data(day=13)
depth_ranges = dict(d.parsed('<int>: <int>'))

# sort smallest modulo first
depth_range_list = sorted([
   (j, (k - 1) * 2) for (j, k) in depth_ranges.items()
], key=lambda x: x[1])


def part1():
    severity = 0
    for j, mod in depth_range_list:
        if j % mod == 0:
            severity += j * depth_ranges[j]

    return severity


def part2():
    for i in count():
        for j, mod in depth_range_list:
            if (i + j) % mod == 0:
                break
        else:
            break

    return i
