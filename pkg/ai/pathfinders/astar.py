from pkg.constants.game import PLAYER_ONE, PLAYER_TWO
from pkg.models.board import Board


class Node:
    _id: int = None
    _x: int = None
    _y: int = None
    _cost = None
    _previous = None

    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._id = y * 666 + x

    def __eq__(self, other):
        return self._id == other.get_id()

    def __str__(self):
        return f'({self._x}, {self._y})'

    def __repr__(self):
        return self.__str__()

    def get_id(self):
        return self._id

    def get_x(self):
        return self._x

    def set_x(self, x):
        self._x = x

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y

    def get_cost(self):
        return self._cost

    def set_cost(self, cost):
        self._cost = cost

    def get_previous(self):
        return self._previous

    def set_previous(self, previous):
        self._previous = previous


def choose_node(nodes):
    return nodes[0]


class AStar:
    _board: Board = None

    def __init__(self, board):
        self.set_board(board)

    def set_board(self, board):
        self._board = board

    def find_path(self, for_player, src_x, src_y, dst_x, dst_y):
        board = self._board
        goal_node = Node(dst_x, dst_y)
        opponent = PLAYER_ONE if for_player == PLAYER_TWO else PLAYER_TWO
        reachable = [Node(src_x, src_y)]
        explored = []
        while len(reachable) > 0:
            node = choose_node(reachable)
            if node == goal_node:
                return

            reachable.remove(node)
            explored.append(node)
            new_reachable = [Node(x, y) for (x, y) in board.get_cell_neighbors(node.get_x(), node.get_y(), [opponent])]
            new_reachable = [n for n in filter(lambda n: n not in explored, new_reachable)]

            for adjacent in new_reachable:
                if adjacent not in reachable:
                    reachable.append(adjacent)

        pass
