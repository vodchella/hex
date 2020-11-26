from pkg.ai.pathfinders import Node, INFINITY
from pkg.constants.game import PLAYER_ONE, PLAYER_TWO
from pkg.models.board import Board


def build_path(to_node: Node):
    path = []
    while to_node is not None:
        path.append((to_node.x(), to_node.y()))
        to_node = to_node.get_previous()
    return path


def to_nodes(cells, cost):
    return [Node(x, y, cost=cost) for (x, y) in cells]


class BasicPathfinder:
    _board: Board = None
    _choose_node_fn = None

    def __init__(self, board, choose_node_fn):
        self._board = board
        self._choose_node_fn = choose_node_fn

    def find_path(self, for_player, src_x, src_y, dst_x, dst_y):
        board = self._board
        dst_node = Node(dst_x, dst_y)
        opponent = PLAYER_ONE if for_player == PLAYER_TWO else PLAYER_TWO
        reachable = [Node(src_x, src_y)]
        explored = []

        while len(reachable) > 0:
            node = self._choose_node_fn(board, reachable, dst_node)
            if node == dst_node:
                return build_path(node)

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

        return []
