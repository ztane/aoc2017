from helpers import get_aoc_data

d = get_aoc_data(day=5)


def part1():
    data = list(d.extract_ints)
    ip = 0
    steps = 0
    try:
        while True:
            increment = data[ip]
            data[ip] += 1
            ip += increment
            steps += 1
    except IndexError:
        return steps


def part2():
    data = list(d.extract_ints)
    ip = 0
    steps = 0
    try:
        while True:
            increment = data[ip]
            if increment >= 3:
                data[ip] -= 1
            else:
                data[ip] += 1
            ip += increment
            steps += 1
    except IndexError:
        return steps
