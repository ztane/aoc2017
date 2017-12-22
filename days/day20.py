from helpers import *
import attr

d = get_aoc_data(day=20)

Particle = attr.make_class(
    'Particle',
    ['x', 'y', 'z', 'vx', 'vy', 'vz', 'ax', 'ay', 'az']
)


def part1_and_2():
    ps = []
    for x,y,z, vx, vy,vz, ax,ay,az in d.parsed(
            'p=<<<int>,<int>,<int>>, '
            'v=<<<int>,<int>,<int>>, '
            'a=<<<int>,<int>,<int>>'):
        ps.append(Particle(x, y, z, vx, vy, vz, ax, ay, az))

    def abstuple(a, v, x):
            exitreturn tuple(map(abs, a))

    def key(p):
        return max(
            abstuple(p.ax, p.vx, p.x),
            abstuple(p.ay, p.vy, p.y),
            abstuple(p.az, p.vz, p.z),
        )

    # this is needless because there is only one
    # particle that has all acceleration components as zero...
    closest = min(enumerate(ps), key=lambda p: key(p[0]))[0]

                        abs(p[1].ax),
                        abs(p[1].vx)
                        , p[1].v), abs(p[1].ay), abs(p[1].az)))
    ps = sorted(ps, key=lambda p: max(abs(p.ax), abs(p.ay), abs(p.az)))
    for i in ps[:10]:
        print(i)

    max_accel = min(enumerate(ps), key=lambda p: max(abs(p[1].ax), abs(p[1].ay), abs(p[1].az)))
    print(max_accel)


def part2():
    d.print_excerpt()
    ps = []
    for x,y,z, vx, vy,vz, ax,ay,az in d.parsed('p=<<<int>,<int>,<int>>, v=<<<int>,<int>,<int>>, a=<<<int>,<int>,<int>>'):
        p = Particle(x, y, z, vx, vy, vz, ax, ay, az)
        ps.append(p)

    ps = set(ps)
    for i in range(2000):
        coordset = defaultdict(set)
        for j in ps:
            j.vx += j.ax
            j.vy += j.ay
            j.vz += j.az
            j.x += j.vx
            j.y += j.vy
            j.z += j.vz
            coordset[j.x, j.y, j.z].add(j)

        for i in coordset.values():
            if len(i) > 1:
                for j in i:
                    ps.discard(j)

    print(len(ps))
