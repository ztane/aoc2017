from helpers import *

d = get_aoc_data(day=6)


def part1_and_2():
    memory = ring_list(d.extract_ints)
    seen = {tuple(memory)}
    first_in_cycle = None
    cycle_start = None
    cycle_length = 0
    get_second = op.itemgetter(1)

    for step in count(1):
        cell, value = max(enumerate(memory), key=get_second)
        memory[cell] = 0

        for i in range(1, value + 1):
            memory[cell + i] += 1

        state = tuple(memory)
        if cycle_start is not None:
            cycle_length += 1

            if state == first_in_cycle:
                return cycle_start, cycle_length

        elif state in seen:
            first_in_cycle = state
            cycle_start = step

        seen.add(state)
