from helpers import *

d = get_aoc_data(day=8)


def part1_and_2():
    regs = defaultdict(int)
    absolute_maximum = 0
    for tgt, op1, val, cond, op2, val2 in d.parsed(
            '<> <str:inc|dec> <int> if <> <> <int>'):
        # __builtins__ gets injected into `globals`!
        if eval(f'{cond} {op2} {val2}', {}, regs):
            regs[tgt] = {'inc': op.add, 'dec': op.sub}[op1](regs[tgt], val)
            absolute_maximum = max(max(regs.values()), absolute_maximum)

    return max(regs.values()), absolute_maximum
