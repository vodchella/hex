import sys
from pkg.constants.game import PLAYER_ONE, PLAYER_TWO
from pkg.models.board import Board
from pkg.utils.hex import get_distance

INFINITY = sys.maxsize


class Node:
    _id: int = None
    _x: int = None
    _y: int = None
    _cost = 0
    _previous = None

    def __init__(self, x, y, cost=0):
        self._x = x
        self._y = y
        self._id = y * 666 + x
        self._cost = cost

    def __eq__(self, other):
        return self._id == other.id()

    def __str__(self):
        cost = 'INF' if self._cost == INFINITY else self._cost
        return f'({self._x}, {self._y}; c={cost})'

    def __repr__(self):
        return self.__str__()

    def id(self):
        return self._id

    def x(self):
        return self._x

    def y(self):
        return self._y

    def get_cost(self):
        return self._cost

    def set_cost(self, cost):
        self._cost = cost

    def get_previous(self):
        return self._previous

    def set_previous(self, previous):
        self._previous = previous


def choose_node(nodes, dst_node: Node):
    min_cost = INFINITY
    best_node = None

    for node in nodes:
        cost_start_to_node = node.get_cost()
        cost_node_to_goal = get_distance(node.x(), node.y(), dst_node.x(), dst_node.y())
        total_cost = cost_start_to_node + cost_node_to_goal

        if min_cost > total_cost:
            min_cost = total_cost
            best_node = node

    return best_node


def to_nodes(cells, cost):
    return [Node(x, y, cost=cost) for (x, y) in cells]


class AStar:
    _board: Board = None

    def __init__(self, board):
        self.set_board(board)

    def set_board(self, board):
        self._board = board

    def find_path(self, for_player, src_x, src_y, dst_x, dst_y):
        board = self._board
        dst_node = Node(dst_x, dst_y)
        opponent = PLAYER_ONE if for_player == PLAYER_TWO else PLAYER_TWO
        reachable = [Node(src_x, src_y)]
        explored = []

        while len(reachable) > 0:
            node = choose_node(reachable, dst_node)
            if node == dst_node:
                return

            reachable.remove(node)
            explored.append(node)

            cells = board.get_cell_neighbors(node.x(), node.y(), exclude_players=[opponent])
            new_reachable = [n for n in filter(lambda n: n not in explored, to_nodes(cells, INFINITY))]

            next_cost = node.get_cost() + 1
            for adjacent in new_reachable:
                if adjacent not in reachable:
                    reachable.append(adjacent)

                if next_cost < adjacent.get_cost():
                    adjacent.set_previous(node)
                    adjacent.set_cost(next_cost)

        pass
