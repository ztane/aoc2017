from helpers import *

d = get_aoc_data(day=22)


def part1():
    the_map = SparseComplexMap(d.lines, default='.')
    position = the_map.center
    direction = -1j
    infections = 0

    for i in range(10000):
        if the_map[position] == '#':
            the_map[position] = '.'
            direction *= 1j
        else:
            the_map[position] = '#'
            infections += 1
            direction *= -1j

        position += direction

    return infections


def part2():
    the_map = SparseComplexMap(d.lines, default='.')
    position = the_map.center
    direction = -1j
    infections = 0

    for i in range(10000000):
        item = the_map[position]
        if item == '#':
            the_map[position] = 'f'
            direction *= 1j
        elif item == 'f':
            the_map[position] = '.'
            direction *= -1
        elif item == 'w':
            the_map[position] = '#'
            infections += 1
        else:
            the_map[position] = 'w'
            direction *= -1j

        position += direction

    return infections
