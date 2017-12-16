from collections import deque

from helpers import get_aoc_data, Parser


ONE_BILLION = 1000_000_000

d = get_aoc_data(day=16)


spin = Parser('s<int>')
exchange = Parser('x<int>/<int>')
partner = Parser('p<str>/<str>')


def initial():
    return deque('abcdefghijklmnop')


def dance(programs):
    for instruction in d.data.split(','):
        if spin(instruction):
            programs.rotate(*spin)
        elif exchange(instruction):
            a, b = exchange
            programs[a], programs[b] = programs[b], programs[a]
        elif partner(instruction):
            a, b = partner
            a = programs.index(a)
            b = programs.index(b)
            programs[a], programs[b] = programs[b], programs[a]
        else:
            raise ValueError(f"Don't know how to execute {instruction}")

    return programs


def part1():
    return ''.join(dance(initial()))


def part2():
    programs = initial()
    seen = {(*programs,): 0}
    counter = 0
    while counter < ONE_BILLION:
        programs = dance(programs)
        final_position = (*programs,)
        counter += 1
        if final_position in seen:
            first_cycle_start = seen[final_position]
            dances_per_cycle = counter - first_cycle_start
            added_cycles = (ONE_BILLION - counter) // dances_per_cycle
            counter += added_cycles * dances_per_cycle

            remaining = ONE_BILLION - counter
            if remaining:
                to_find = first_cycle_start + remaining
                for position, n in seen.items():
                    if n == to_find:
                        programs = position
                        counter += n - first_cycle_start
                        break

            seen = {}
        else:
            seen[final_position] = counter

    assert counter == ONE_BILLION
    return ''.join(programs)
