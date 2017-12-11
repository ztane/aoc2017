from helpers import *

d = get_aoc_data(day=11)


def part1_and_2():
    # http://keekerdc.com/2011/03/hexagon-grids-coordinate-systems-and-distance-calculations/
    vectors = {
        'n':  (1, 0, -1),
        'ne': (1, -1, 0),
        'se': (0, -1, 1),
        's':  (-1, 0, 1),
        'sw': (-1, 1, 0),
        'nw': (0, 1, -1)
    }

    x = y = z = max_d = 0
    for i in d.data.split(','):
        dx, dy, dz = vectors[i]
        x += dx
        y += dy
        z += dz
        max_d = max(max_d, abs(x), abs(y), abs(z))

    return max(abs(x), abs(y), abs(z)), max_d
