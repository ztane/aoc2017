from helpers import *

d = get_aoc_data(day=19)


def part1_and_2():
    the_map = [list(i) for i in d.data.splitlines()]
    x, y = the_map[0].index('|'), 0

    if x == 0:
        print('Warning, pretty shure you run an unpatched aocd!')

    dx, dy = (0, 1)
    found = ''

    ct = 0
    while True:
        if the_map[y][x] == ' ':
            break

        if the_map[y][x] == '+':
            if the_map[y][x + 1] == '-':
                dx, dy = 1, 0
            elif the_map[y][x - 1] == '-':
                dx, dy = -1, 0
            elif the_map[y + 1][x] == '|':
                dx, dy = 0, 1
            elif the_map[y - 1][x] == '|':
                dx, dy = 0, -1
            else:
                raise ValueError('dont know about turn')

        elif the_map[y][x].isalpha():
            found += the_map[y][x]

        ct += 1
        the_map[y][x] = '/'
        y += dy
        x += dx

    return found, ct
