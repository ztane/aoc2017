from helpers import *

d = get_aoc_data(day=7)


class Program:
    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.children = []
        self._total_weight = None
        self.parent = None
        self.descendant_weight = None

    def set_parent(self, parent):
        self.parent = parent

    def add_child(self, child):
        self.children.append(child)
        child.set_parent(self)

    @property
    def total_weight(self):
        if self._total_weight is None:
            self.descendant_weight = sum(
                i.total_weight for i in self.children
            )
            self._total_weight = self.weight + self.descendant_weight

        return self._total_weight

    def get_unbalanced_branch(self):
        unique = find_unique(self.children,
                             lambda x: x.total_weight)
        if not unique:
            return None, None

        for i in self.children:
            if i is not unique:
                return unique, i.total_weight

        raise ValueError(f'Single unique branch {self.name}')

    def find_correct_weight(self, desired_total=None):
        unbalanced, desired_descendant_w = self.get_unbalanced_branch()
        if unbalanced:
            return unbalanced.find_correct_weight(
                desired_total=desired_descendant_w)
        else:
            print(f'{self.name} has no unbalanced branches')
            delta = desired_total - self.total_weight
            return self.weight + delta


def part1_and_2():
    leaf_parser = Parser('<str> (<int>)')
    parent_parser = Parser('<str> (<int>) -> <str>')

    programs_by_name = {}
    child_names = defaultdict(list)
    for i in d.lines:
        if leaf_parser(i):
            name, weight = leaf_parser

        else:
            name, weight, children = parent_parser(i)
            child_names[name] = children.split(', ')

        programs_by_name[name] = Program(name, weight)

    for p in programs_by_name.values():
        for c in child_names[p.name]:
            p.add_child(programs_by_name[c])

    root = None
    for p in programs_by_name.values():
        if not p.parent:
            assert not root
            root = p

    correct_weight = root.find_correct_weight()
    print(f'Root name {root.name}, total weight: {root.total_weight}')
    return root.name, correct_weight
