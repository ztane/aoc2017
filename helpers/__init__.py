# noinspection PyUnresolvedReferences
import operator as op
import re
import typing
# noinspection PyUnresolvedReferences
from collections import *
# noinspection PyUnresolvedReferences
from functools import *
# noinspection PyUnresolvedReferences
from hashlib import md5
# noinspection PyUnresolvedReferences
from heapq import *
# noinspection PyUnresolvedReferences
from itertools import *
from math import *
# noinspection PyUnresolvedReferences
from string import *
from typing import Union, Dict

from aocd import get_data


class reify(object):
    """
    Rip of `reify` from Pyramid framework.

    Use as a class method decorator.  It operates almost exactly like the
    Python ``@property`` decorator, but it puts the result of the method it
    decorates into the instance dict after the first call, effectively
    replacing the function it decorates with an instance variable.  It is, in
    Python parlance, a non-data descriptor.
    """
    def __init__(self, wrapped):
        self.wrapped = wrapped
        update_wrapper(self, wrapped)

    def __get__(self, inst, objtype=None):
        if inst is None:
            return self
        val = self.wrapped(inst)
        setattr(inst, self.wrapped.__name__, val)
        return val


class Data:
    def __init__(self, data: str):
        self.data = data.rstrip('\n\r')

    @reify
    def lines(self) -> typing.Tuple[str, ...]:
        return tuple(filter(bool, map(str.rstrip, self.data.splitlines())))

    def split(self, separator=', ') -> typing.List[str]:
        return self.data.split(separator)

    @reify
    def as_int(self) -> int:
        return int(self.data)

    @reify
    def extract_ints(self) -> typing.Tuple[int, ...]:
        return tuple(map(int, re.findall(r'-?\d+', self.data)))

    @reify
    def sentences(self) -> typing.List[typing.List[str]]:
        """
        Assume the data is

        :return:
        """
        return [
            i.split() for i in self.lines
        ]

    @reify
    def integer_matrix(self) -> typing.List[typing.List[int]]:
        """
        Assume the data is a 2-dimensional space-separated integer matrix

        :return: that matrix
        """
        return [[int(i) for i in line.split()] for line in self.lines]

    def parsed(self, fmt: str, verbatim_ws: bool=False) \
            -> typing.Iterator[typing.Tuple]:
        """
        Return the data parsed with a single parser
        :param fmt: the format
        :param verbatim_ws: whether verbatim boolean is used
        :return: iterator of parsed tuples
        """
        return Parser(fmt, verbatim_ws=verbatim_ws).for_lines(self.lines)

    def print_excerpt(self) -> None:
        """
        Print an excerpt of the data. Maximum of 10 lines followed by
        how many lines were omitted
        :return: None
        """
        lines = self.lines
        for i in lines[:7]:
            print(i)
        if len(lines) > 10:
            print(f'Total {len(lines)} lines; {len(lines) - 7} '
                  f'remaining lines omitted...')


def get_aoc_data(day: int) -> Data:
    """
    Get the wrapped AOC data for a given day

    :param day: the day
    :return: the data
    """
    return Data(get_data(day=day))


def clamp(value: int, min_: int, max_: int) -> int:
    """
    Clamp the value so that it is at least min_ and at most max_

    :param value: the value
    :param min_: the minimum
    :param max_: the maximum
    :return: min_, max_, or value, iff min_ <= value <= max_
    """

    if value < min_:
        return min_
    if value > max_:
        return max_
    return value


def ngrams(n: int, value: Sequence) -> typing.Iterator[Sequence]:
    """
    Given a *sequence*, return its n-grams

    :param value: the value, can be list, tuple, or str
    :return: *generator* of the ngrams
    """

    for i in range(len(value) - n + 1):
        yield value[i:i + n]


def items(thing, *indexes):
    """
    Return the given indexes of the item as a tuple

    :param thing: the thing to index
    :param indexes: indexes
    :return: tuple of the items
    """
    return op.itemgetter(*indexes)(thing)


def to_ints(container):
    """
    Return the given items as ints, in the same container type

    :param container: the items
    :return: the items as ints
    """

    t = type(container)
    return t(map(int, container))


def to_floats(container):
    """
    Return the given items as floats, in the same container type

    :param container: the items
    :return: the items as ints
    """

    t = type(container)
    return t(map(float, container))


def every_nths(iterable, n=2):
    """
    return n lists of every nth elements; first list contains item
    0, second list item 1 and so forth

    :param iterable: the iterable to iterate over. Will be converted
        to a list internally
    :return: list of lists
    """

    as_list = list(iterable)
    return [as_list[i::n] for i in range(n)]


def get_ints(s):
    """
    Return all decimal integers in the given string
    as a sequence

    :param s: a string
    :return: sequence of integers
    """
    return list(map(int, re.findall('\d+', s)))


def draw_display(display_data):
    """
    Draw pixel display (row, column matrix)

    :param display_data: the display data
    :return: None
    """
    row_length = len(display_data[0])
    print('-' * row_length)
    for row in display_data:
        for column in row:
            print([' ', '\033[42m \033[0m'][bool(column)], end='')
        print()
    print('-' * row_length)


_parser_conversions = {
    'int': (int, '-?\d+'),
    'str': (str, '.*?'),
}


class Parser:
    """
    A parser class for parsing fields from a single
    formatted input string.
    """
    last_val = None

    def __init__(self, fmt, verbatim_ws=False):
        """
        Initialize the parser class, with given format

        :param fmt: the format string
        :param verbatim_ws: if false, spaces are replaced with
            \s+, if true, space characters must match exactly
        """
        regex = ''
        pos = 0

        self.matched = False
        self.items = ()
        self.conversions = []

        while pos < len(fmt):
            c = fmt[pos]
            pos += 1
            if c == '<':
                if fmt[pos] == '<':
                    regex += r'\<'
                    pos += 1
                else:
                    end = fmt.index('>', pos)
                    pattern = fmt[pos:end] or 'str'
                    conversion, _, pattern = pattern.partition(':')
                    convfunc, default_re = _parser_conversions[conversion]
                    if not pattern:
                        pattern = default_re
                    regex += '({})'.format(pattern)
                    self.conversions.append(convfunc)
                    pos = end + 1

            else:
                if c == ' ' and not verbatim_ws:
                    regex += r'\s+'
                else:
                    regex += re.escape(c)

        self.regex = re.compile(regex)

    def __call__(self, string):
        """
        Match the given string agains the pattern, and set results
        :param string: the string
        :return: self for chaining and truth-value checking
        """
        m = self.regex.fullmatch(string)
        self.matched = bool(m)
        self.last_val = string
        if m:
            self.items = tuple(
                self._convert(m, convfunc, group)
                for (group, convfunc) in enumerate(self.conversions, 1))
        else:
            self.items = ()

        return self

    def for_lines(self, lines):
        for line in lines:
            yield tuple(self(line))

    def _convert(self, match, convfunc, group):
        val = match.group(group)
        if val is not None:
            return convfunc(val)
        return None

    def __bool__(self):
        return self.matched

    def __iter__(self):
        if not self.matched:
            raise ValueError(
                'The pattern didn\'t match {}'.format(self.last_val))

        return iter(self.items)

    def __len__(self):
        if not self.matched:
            raise ValueError('The pattern didn\'t match')

        return len(self.items)

    def __getitem__(self, i):
        if not self.matched:
            raise ValueError('The pattern didn\'t match')

        return self.items[i]


@total_ordering
class Node:
    __slots__ = ('heuristic', 'distance', 'state')

    def __init__(self, heuristic, distance, state):
        self.heuristic = heuristic
        self.distance = distance
        self.state = state

    def __eq__(self, other):
        return ((self.heuristic, self.distance) ==
                (other.heuristic, other.distance))

    def __lt__(self, other):
        return self.heuristic + self.distance < other.heuristic + other.distance

    def __iter__(self):
        return iter((self.heuristic, self.distance, self.state))


def neighbourhood_4(x, y, valid=lambda x, y: True):
    neighbours = []
    for nx, ny in ((x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)):
        if valid(nx, ny):
            neighbours.append((nx, ny))

    return neighbours


def a_star_solve(origin,
                 *,
                 target=None,
                 max_distance=None,
                 neighbours,
                 heuristic=None,
                 is_target=None,
                 find_all=False,
                 hashable=lambda n: n):
    if max_distance is None:
        max_distance = 2 ** 32

    if not heuristic:
        def heuristic(node, target):
            return 0

    queue = [Node(heuristic(origin, target), 0, origin)]
    visited = {hashable(origin)}

    if not is_target:
        def is_target(n):
            return n == target

    cnt = 0
    all_routes = []
    max_depth = 0

    min_h = heuristic(origin, target) + 1
    while queue:
        hx, distance, node = heappop(queue)
        if is_target(node):
            if not find_all:
                return distance, node
            else:
                all_routes.append((distance, node))
                continue

        visited.add(hashable(node))
        if distance > max_depth:
            max_depth = distance

        for d_dist, node in neighbours(node):
            if hashable(node) in visited:
                continue

            if distance + d_dist <= max_distance:
                h = heuristic(node, target)
                if h < min_h:
                    min_h = h
                heappush(queue, Node(h,
                                     distance + d_dist, node))
                cnt += 1

    print(cnt, 'iterations')
    if find_all:
        return all_routes
    return len(visited)


chained = chain.from_iterable


def lcm(a: int, b: int) -> int:
    """
    Returns the least common multiple of the 2 numbers
    :param a: number
    :param b: another
    :return: the lcm
    """
    return (a * b) // gcd(a, b)


def better_translator(table: Dict[str, str]) -> typing.Callable[[str], str]:
    """
    Returns a translator function that, given a string, will replace all
    the key strings to their corresponding values from the string, using
    maximal munch.

    :param table: the dictionary of strings to strings
    :return: a function, str->str
    """
    strings = '|'.join(re.escape(i) for i in table.keys())
    pattern = re.compile(strings)

    def replacement(m):
        return table[m.group(0)]

    def translate(s):
        return pattern.sub(replacement, s)

    return translate


def md5digest(s: Union[bytes, str]) -> str:
    """
    Return the md5 digest of the given argument as hex
    :param s: the string; either bytes or str
    :return: the hex digest, as a string
    """
    try:
        s = s.encode()
    except AttributeError:
        pass

    return md5(s).hexdigest()


def cinf_norm(val: complex) -> int:
    """
    Calculate the L_inf norm of the given complex number as an integer
    :param val: the number
    :return: the norm
    """
    return int(max(abs(val.real), abs(val.imag)))


def cmanhattan(val: complex) -> int:
    """
    Calculate the L_1 norm of the given complex number as an integer
    :param val: the number
    :return: the norm
    """
    return int(abs(val.real) + abs(val.imag))


def spiral_walk() -> typing.Iterator[complex]:
    """
    Return the generator of the spiral walk, as in AOC 2017 puzzle 3.
    :return: the generator that yields successive coordinates as complex numbers
    in order.
    """
    coords = 0 + 0j
    direction = 1
    for max_d in count():
        # OEIS A022144
        looping = (2 * max_d + 1) ** 2 - (2 * max_d - 1) ** 2
        for i in range(looping):
            yield coords
            if cinf_norm(coords + direction) > max_d:
                direction *= 1j

            coords += direction

        coords += 1 - direction
        direction = 1


_CNEIGHBOURHOOD_8_WITH_SELF = list(x + y * 1j
                                   for (x, y)
                                   in product([-1, 0, 1], repeat=2))
_CNEIGHBOURHOOD_8 = [i for i in _CNEIGHBOURHOOD_8_WITH_SELF if i]


def cneighbours_8(point: complex,
                  *,
                  add_self: bool=False) -> typing.Iterator[complex]:
    """
    Return the 8-neighbourhood around the complex coordinates. If `add_self`
    is true, then return the point itself as well.

    :param add_self: boolean, add self into the value
    :return: a generator of neighbour coordinates
    """

    for delta in ((_CNEIGHBOURHOOD_8, _CNEIGHBOURHOOD_8_WITH_SELF)[add_self]):
        yield point + delta


class ring_list(list):
    """
    Fixed length list, with modular indexing
    """

    def __delitem__(self, key):
        raise NotImplemented

    def pop(self, *a, **kw):
        raise NotImplemented

    def __getitem__(self, item):
        return super().__getitem__(item % len(self))

    def __setitem__(self, item, value):
        return super().__setitem__(item % len(self), value)
