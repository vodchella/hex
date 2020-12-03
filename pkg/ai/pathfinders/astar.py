from pkg.ai.pathfinders import Node, INFINITY
from pkg.ai.pathfinders.basic import BasicPathfinder
from pkg.utils.hex import get_distance


class AStarPathfinder(BasicPathfinder):
    def __init__(self, board):
        super().__init__(board)

    def choose_node(self, nodes, dst_node: Node):
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
