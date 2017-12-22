import threading

from helpers import *

d = get_aoc_data(day=18)

snd = Parser('snd <>')
set = Parser('set <> <>')
add = Parser('add <> <>')
mul = Parser('mul <> <>')
mod = Parser('mod <> <>')
rcv = Parser('rcv <>')
jgz = Parser('jgz <> <>')


last_freq = None
first_frequency = None


def parse_code(lines, registers):
    memory = []
    for i in lines:
        if snd(i):
            freq, = snd

            @memory.append
            def instr(src=accessor(freq)):
                global last_freq
                last_freq = src()

        elif set(i):
            reg, val = set

            @memory.append
            def instr(reg=reg, val=accessor(val)):
                registers[reg] = val()

        elif add(i):
            a, b = add

            @memory.append
            def instr(a=a, b=accessor(b)):
                registers[a] += b()

        elif mul(i):
            a, b = mul

            @memory.append
            def instr(a=a, b=accessor(b)):
                registers[a] *= b()

        elif mod(i):
            a, b = mod

            @memory.append
            def instr(a=a, b=accessor(b)):
                registers[a] %= b()

        elif rcv(i):
            reg, = rcv

            @memory.append
            def instr(reg=accessor(reg)):
                global first_frequency
                if reg() and first_frequency is None:
                    print('LAST FREQUENCY', last_freq)
                    first_frequency = last_freq

        elif jgz(i):
            reg, offset = jgz

            @memory.append
            def instr(reg=accessor(reg), offset=accessor(offset)):
                global ip
                if reg() > 0:
                    ip += offset() - 1

        else:
            print('failing instruction', i)
            exit(1)

    @memory.append
    def hlt():
        print('Completed. a={}'.format(registers['a']))
        return True

    return memory


ips = [0, 0]
send_ctrs = [0, 0]
waiting = [False, False]


def parse_code2(lines, recv_queue, send_queue, registers, program_number):
    def accessor(operand):
        if operand.isalpha():
            return lambda: registers[operand]
        else:
            val = int(operand)
            return lambda: val

    memory = []
    for i in lines:
        if snd(i):
            freq, = snd

            @memory.append
            def instr(src=accessor(freq)):
                send_queue.append(src())
                send_ctrs[program_number] += 1

        elif set(i):
            reg, val = set

            @memory.append
            def instr(reg=reg, val=accessor(val)):
                registers[reg] = val()

        elif add(i):
            a, b = add

            @memory.append
            def instr(a=a, b=accessor(b)):
                registers[a] += b()

        elif mul(i):
            a, b = mul

            @memory.append
            def instr(a=a, b=accessor(b)):
                registers[a] *= b()

        elif mod(i):
            a, b = mod

            @memory.append
            def instr(a=a, b=accessor(b)):
                registers[a] %= b()

        elif rcv(i):
            reg, = rcv

            @memory.append
            def instr(reg=reg):
                while not recv_queue:
                    waiting[program_number] = True
                    if all(waiting) and not any(queues):
                        raise Exception('Value {}'.format(send_ctrs))
                waiting[program_number] = False
                registers[reg] = recv_queue.pop(0)

        elif jgz(i):
            reg, offset = jgz

            @memory.append
            def instr(reg=accessor(reg), offset=accessor(offset)):
                global ip
                if reg() > 0:
                    ips[program_number] += offset() - 1

        else:
            print('failing instruction', i)
            exit(1)

    @memory.append
    def hlt():
        print('Completed. a={}'.format(registers['a']))
        return True

    return memory


q1 = []
q2 = []
queues = [q1, q2]

memory = [parse_code2(d.lines,
                      recv_queue=q1,
                      send_queue=q2,
                      registers=defaultdict(int),
                      program_number=0),
          parse_code2(d.lines,
                      recv_queue=q2,
                      send_queue=q1,
                      registers=defaultdict(int, p=1),
                      program_number=1)]


def run(program_number):
    while not memory[program_number][ips[program_number]]():
        ips[program_number] += 1


def part1():
    return


def part2():
    t1 = threading.Thread(target=run, args=(0,))
    t2 = threading.Thread(target=run, args=(1,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(send_ctrs[1])
