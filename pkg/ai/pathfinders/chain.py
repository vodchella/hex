from pkg.ai.pathfinders import Node, INFINITY, to_nodes
from pkg.ai.pathfinders.astar import AStarPathfinder
from pkg.ai.pathfinders.basic import BasicPathfinder
from pkg.constants.game import PLAYER_NONE, PLAYER_ONE, PLAYER_TWO
from pkg.utils.hex import get_distance


class ChainPathfinder(BasicPathfinder):
    _astar: AStarPathfinder = None
    _chains = {}
    _chain_paths = {}

    def __init__(self, board):
        super().__init__(board)
        self._astar = AStarPathfinder(board)
        self._chains = {
            PLAYER_ONE: [(i, c) for i, c in enumerate(self._find_chains(PLAYER_ONE))],
            PLAYER_TWO: [(i, c) for i, c in enumerate(self._find_chains(PLAYER_TWO))],
        }
        self._chain_paths = {
            PLAYER_ONE: self._find_paths_between_all_chains(PLAYER_ONE),
            PLAYER_TWO: self._find_paths_between_all_chains(PLAYER_TWO),
        }

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
                            new_reachable = [n for n in filter(lambda n: n not in explored, to_nodes(cells))]
                            for adjacent in new_reachable:
                                if adjacent not in reachable:
                                    reachable.append(adjacent)
                        if len(chain):
                            result.append(chain)
        return result

    def _find_paths_between_all_chains(self, for_player):
        result = []
        chains = self._chains[for_player]
        if len(chains) > 1:
            processed = []
            for (i, chain_from) in chains:
                processed.append(i)
                for (j, chain_to) in filter(lambda c: c[0] not in processed, chains):
                    path, node_from, node_to = self._find_path_between_two_chains(for_player, chain_from, chain_to)
                    if len(path):
                        result.append((i, j, path, node_from, node_to))
        return result

    def _find_path_between_two_chains(self, for_player, chain_from, chain_to):
        shortest_path_len = INFINITY
        shortest_path = []
        best_node_from = None
        best_node_to = None
        for node_from in chain_from:
            for node_to in chain_to:
                path = self._astar.find_path(for_player, node_from.x(), node_from.y(), node_to.x(), node_to.y())
                path_len = len(path)
                if path_len == 0:
                    break
                if path_len < shortest_path_len:
                    shortest_path_len = path_len
                    shortest_path = path
                    best_node_from = node_from
                    best_node_to = node_to
        return shortest_path[1:-1], best_node_from, best_node_to

    def choose_node(self, nodes, dst_node: Node):
        min_cost = INFINITY
        best_node = None

        for node in nodes:
            player = self._board.get_cell(node.x(), node.y())
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

    def find_path(self, for_player, src_x, src_y, dst_x, dst_y):
        board = self._board
        path = super().find_path(for_player, src_x, src_y, dst_x, dst_y)
        return [(x, y) for (x, y) in filter(lambda c: board.get_cell(c[0], c[1]) == PLAYER_NONE, path)]
