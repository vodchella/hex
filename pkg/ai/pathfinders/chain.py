from pkg.ai.pathfinders import Node, INFINITY, to_nodes
from pkg.ai.pathfinders.basic import BasicPathfinder
from pkg.constants.game import PLAYER_NONE, PLAYER_ONE, PLAYER_TWO
from pkg.models.board import Board
from pkg.utils.hex import get_distance


def choose_node(board: Board, nodes, dst_node: Node):
    min_cost = INFINITY
    best_node = None

    for node in nodes:
        player = board.get_cell(node.x(), node.y())
        if player != PLAYER_NONE:
            total_cost = 0
            node.set_cost(0)
        else:
            cost_start_to_node = node.get_cost()
            cost_node_to_goal = get_distance(node.x(), node.y(), dst_node.x(), dst_node.y())
            total_cost = cost_start_to_node + cost_node_to_goal

        if min_cost > total_cost:
            min_cost = total_cost
            best_node = node

    return best_node


class ChainPathfinder(BasicPathfinder):
    def __init__(self, board):
        super().__init__(board, choose_node)

    def _find_chains(self, for_player):
        result = []
        opponent = PLAYER_ONE if for_player == PLAYER_TWO else PLAYER_TWO
        explored = []
        board = self._board
        w, h = board.get_dimensions()
        for y in range(h):
            for x in range(w):
                current_node = Node(x, y)
                if current_node not in explored:
                    player = board.get_cell(x, y)
                    if player == for_player:
                        chain = []
                        reachable = [current_node]
                        while len(reachable) > 0:
                            node = reachable[0]
                            reachable.remove(node)
                            explored.append(node)
                            chain.append(node)
                            cells = board.get_cell_neighbors(node.x(), node.y(), [opponent, PLAYER_NONE])
                            new_reachable = [n for n in filter(lambda n: n not in explored, to_nodes(cells, INFINITY))]
                            for adjacent in new_reachable:
                                if adjacent not in reachable:
                                    reachable.append(adjacent)
                        result.append(chain)
        return result

    def find_path(self, for_player, src_x, src_y, dst_x, dst_y):
        print(self._find_chains(for_player))
        board = self._board
        path = super().find_path(for_player, src_x, src_y, dst_x, dst_y)
        return [(x, y) for (x, y) in filter(lambda c: board.get_cell(c[0], c[1]) == PLAYER_NONE, path)]
