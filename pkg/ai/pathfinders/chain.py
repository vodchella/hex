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
        best_from_node = None
        best_to_node = None
        for from_node in chain_from:
            path, best_node = self._find_path_from_node_to_chain(for_player, from_node, chain_to)
            path_len = len(path)
            if path_len == 0:
                break
            if path_len < shortest_path_len:
                shortest_path_len = path_len
                shortest_path = path
                best_from_node = from_node
                best_to_node = best_node
        return shortest_path, best_from_node, best_to_node

    def _find_path_from_node_to_chain(self, for_player, from_node, to_chain):
        shortest_path_len = INFINITY
        shortest_path = []
        best_node = None
        for to_node in to_chain:
            path = self._astar.find_path(for_player, from_node.x(), from_node.y(), to_node.x(), to_node.y())
            path_len = len(path)
            if path_len == 0:
                break
            if path_len < shortest_path_len:
                shortest_path_len = path_len
                shortest_path = path
                best_node = to_node
        return shortest_path[1:-1], best_node

    def _find_nearest_chain_to_node(self, for_player, node):
        shortest_path_len = INFINITY
        shortest_path = []
        best_node = None
        best_chain_id = None
        chains = self._chains[for_player]
        for i, chain in chains:
            path, dst_node = self._find_path_from_node_to_chain(for_player, node, chain)
            if dst_node is None:
                break
            path_len = len(path)
            if path_len < shortest_path_len:
                shortest_path_len = path_len
                shortest_path = path
                best_node = dst_node
                best_chain_id = i
        return best_chain_id, shortest_path, best_node

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
        from_node = Node(src_x, src_y)
        to_node = Node(dst_x, dst_y)

        simple_path = self._astar.find_path(for_player, src_x, src_y, dst_x, dst_y)

        src_chain_id, src_path, _ = self._find_nearest_chain_to_node(for_player, from_node)
        dst_chain_id, dst_path, _ = self._find_nearest_chain_to_node(for_player, to_node)

        if src_chain_id is not None and dst_chain_id is not None:
            if src_chain_id == dst_chain_id:
                path = [from_node.tuple()] + src_path + dst_path + [to_node.tuple()]
                return path if len(path) < len(simple_path) else simple_path
            else:
                pass
        else:
            return simple_path

        path = super().find_path(for_player, src_x, src_y, dst_x, dst_y)
        return [(x, y) for (x, y) in filter(lambda c: board.get_cell(c[0], c[1]) == PLAYER_NONE, path)]
