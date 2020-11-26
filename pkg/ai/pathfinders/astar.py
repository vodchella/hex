from pkg.ai.pathfinders import Node, INFINITY
from pkg.ai.pathfinders.basic import BasicPathfinder
from pkg.models.board import Board
from pkg.utils.hex import get_distance


def choose_node(board: Board, nodes, dst_node: Node):
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


class AStarPathfinder:
    _pathfinder: BasicPathfinder = None

    def __init__(self, board):
        self._pathfinder = BasicPathfinder(board, choose_node)

    def find_path(self, for_player, src_x, src_y, dst_x, dst_y):
        return self._pathfinder.find_path(for_player, src_x, src_y, dst_x, dst_y)
