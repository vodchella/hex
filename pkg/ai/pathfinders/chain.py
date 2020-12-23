from functools import reduce
from pkg.ai.pathfinders import Node, INFINITY, to_nodes
from pkg.ai.pathfinders.astar import AStarPathfinder
from pkg.ai.pathfinders.basic import BasicPathfinder
from pkg.constants.game import PLAYER_NONE, PLAYER_ONE, PLAYER_TWO
from pkg.utils.paths import merge_paths


class ChainPathfinder(BasicPathfinder):
    _astar: AStarPathfinder = None
    _chains = {}
    _chain_paths = {
        PLAYER_ONE: [],
        PLAYER_TWO: [],
    }

    def __init__(self, board):
        super().__init__(board)
        self._astar = AStarPathfinder(board)
        self._chains = {
            PLAYER_ONE: [(i, c) for i, c in enumerate(self._find_chains(PLAYER_ONE))],
            PLAYER_TWO: [(i, c) for i, c in enumerate(self._find_chains(PLAYER_TWO))],
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

    def _find_path_between_chains(self, for_player, src_chain_id: int, dst_chain_id: int):
        def recursive(c_path):
            if c_path[1] == dst_chain_id:
                return [c_path]
            else:
                r = [c_path]
                s_paths = [p for p in filter(lambda cp: cp[0] == c_path[1], chain_paths)]
                for sp in s_paths:
                    r += recursive(sp)
                return r

        shortest_path_len = INFINITY
        shortest_path = []
        chain_paths = self._chain_paths[for_player]
        starting_paths = [p for p in filter(lambda cp: cp[0] == src_chain_id, chain_paths)]
        for chain_path in starting_paths:
            path = recursive(chain_path)
            do_reduce = len(path) > 1
            path_len = reduce(lambda a, b: len(a[2]) + len(b[2]), path) if do_reduce else len(path[0][2])
            if path_len < shortest_path_len:
                shortest_path_len = path_len
                shortest_path = reduce(lambda a, b: a[2] + b[2], path) if do_reduce else path[0][2]

        return shortest_path

    def find_path(self, for_player, src_x, src_y, dst_x, dst_y):
        from_node = Node(src_x, src_y)
        to_node = Node(dst_x, dst_y)

        self._chain_paths[for_player] = self._find_paths_between_all_chains(for_player)

        shortest_path = self._astar.find_path(for_player, src_x, src_y, dst_x, dst_y)
        if len(shortest_path) > 2:
            chains = self._chains[for_player]
            for i1, chain1 in chains:
                beg_path, n1 = self._find_path_from_node_to_chain(for_player, from_node, chain1)
                if n1 is not None:
                    for i2, chain2 in chains:
                        end_path, n2 = self._find_path_from_node_to_chain(for_player, to_node, chain2)
                        if n2 is not None:
                            if i1 == i2:
                                path = merge_paths([from_node.tuple()], beg_path, end_path, [to_node.tuple()])
                            else:
                                path = self._find_path_between_chains(for_player, i1, i2)
                                path = merge_paths([from_node.tuple()], beg_path, path, end_path, [to_node.tuple()])
                            if len(path) < len(shortest_path):
                                shortest_path = path

        return shortest_path
