import sys

INFINITY = sys.maxsize


class Node:
    _id: int = None
    _x: int = None
    _y: int = None
    _cost = 0
    _previous = None
    _render_cost = False

    def __init__(self, x, y, cost=0, render_cost=False):
        self._x = x
        self._y = y
        self._id = y * 666 + x
        self._cost = cost
        self._render_cost = render_cost

    def __eq__(self, other):
        return self._id == other.id()

    def __str__(self):
        cost_str = ''
        if self._render_cost:
            cost = 'INF' if self._cost == INFINITY else self._cost
            cost_str = f'; c={cost}'
        return f'({self._x}, {self._y}{cost_str})'

    def __repr__(self):
        return self.__str__()

    def id(self):
        return self._id

    def x(self):
        return self._x

    def y(self):
        return self._y

    def tuple(self):
        return self._x, self._y

    def get_cost(self):
        return self._cost

    def set_cost(self, cost):
        self._cost = cost

    def get_previous(self):
        return self._previous

    def set_previous(self, previous):
        self._previous = previous


def to_nodes(cells, cost=INFINITY):
    return [Node(x, y, cost=cost) for (x, y) in cells]
