from functools import reduce
from pkg.ai.pathfinders import Node, INFINITY, to_nodes
from pkg.ai.pathfinders.astar import AStarPathfinder
from pkg.ai.pathfinders.basic import BasicPathfinder
from pkg.constants.game import PLAYER_NONE, PLAYER_ONE, PLAYER_TWO
from pkg.utils.paths import merge_paths


class ChainPathfinder(BasicPathfinder):
    _for_player = None
    _dst_node = None
    _astar: AStarPathfinder = None
    _chains = []
    _chain_paths = []

    def __init__(self, board):
        super().__init__(board)
        self._astar = AStarPathfinder(board)

    def _find_chains(self):
        result = []
        opponent = PLAYER_ONE if self._for_player == PLAYER_TWO else PLAYER_TWO
        explored = []
        board = self._board
        w, h = board.get_dimensions()
        for y in range(h):
            for x in range(w):
                current_node = Node(x, y)
                if current_node not in explored:
                    player = board.get_cell(x, y)
                    if player == self._for_player:
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

    def _find_paths_between_all_chains(self):
        result = []
        if len(self._chains) > 1:
            processed = []
            for (i, chain_from) in self._chains:
                processed.append(i)
                for (j, chain_to) in filter(lambda c: c[0] not in processed, self._chains):
                    path, node_from, node_to = self._find_path_between_two_chains(chain_from, chain_to)
                    if len(path):
                        result.append((i, j, path, node_from, node_to))
        return result

    def _find_path_between_two_chains(self, chain_from, chain_to):
        shortest_path_len = INFINITY
        shortest_path = []
        best_from_node = None
        best_to_node = None
        for from_node in chain_from:
            path, best_node = self._find_path_from_node_to_chain(from_node, chain_to)
            path_len = len(path)
            if path_len == 0:
                break
            if path_len < shortest_path_len:
                shortest_path_len = path_len
                shortest_path = path
                best_from_node = from_node
                best_to_node = best_node
        return shortest_path, best_from_node, best_to_node

    def _find_path_from_node_to_chain(self, from_node, to_chain):
        shortest_path_len = INFINITY
        shortest_path_to_dst_len = INFINITY
        shortest_path = []
        best_node = None
        for to_node in to_chain:
            path = self._astar.find_path(
                self._for_player,
                from_node.x(),
                from_node.y(),
                to_node.x(),
                to_node.y()
            )
            path_len = len(path)
            if path_len == 0:
                break
            if path_len <= shortest_path_len:
                the_best = True
                path_to_dst = self._astar.find_path(
                    self._for_player,
                    to_node.x(),
                    to_node.y(),
                    self._dst_node.x(),
                    self._dst_node.y()
                )
                path_to_dst_len = len(path_to_dst)
                if path_to_dst_len > 0:
                    if path_to_dst_len < shortest_path_to_dst_len:
                        shortest_path_to_dst_len = path_to_dst_len
                    else:
                        the_best = False

                if the_best:
                    shortest_path_len = path_len
                    shortest_path = path
                    best_node = to_node

        return shortest_path[1:-1], best_node

    def _find_path_between_chains(self, src_chain_id: int, dst_chain_id: int):
        def recursive(c_path):
            if c_path[1] == dst_chain_id:
                return [c_path]
            else:
                r = [c_path]
                s_paths = [p for p in filter(lambda cp: cp[0] == c_path[1], self._chain_paths)]
                for sp in s_paths:
                    r += recursive(sp)
                return r

        shortest_path_len = INFINITY
        shortest_path = []
        starting_paths = [p for p in filter(lambda cp: cp[0] == src_chain_id, self._chain_paths)]
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

        def is_free_cell(cell):
            return self._board.get_cell(cell[0], cell[1]) == PLAYER_NONE

        def finalize_path(path_to_finalize):
            beg = from_node.tuple()
            end = to_node.tuple()
            beg_p = [beg] if is_free_cell(beg) else []
            end_p = [end] if is_free_cell(end) else []
            return merge_paths(beg_p, path_to_finalize, end_p)

        self._dst_node = to_node
        self._for_player = for_player
        self._chains = [(i, c) for i, c in enumerate(self._find_chains())]
        self._chain_paths = self._find_paths_between_all_chains()

        shortest_path = self._astar.find_path(for_player, src_x, src_y, dst_x, dst_y)
        shortest_path = [p for p in filter(lambda c: is_free_cell(c), shortest_path)]

        if len(shortest_path) > 2:
            for i1, chain1 in self._chains:
                beg_path, n1 = self._find_path_from_node_to_chain(from_node, chain1)
                if n1 is not None:
                    for i2, chain2 in self._chains:
                        end_path, n2 = self._find_path_from_node_to_chain(to_node, chain2)
                        if n2 is not None:
                            if i1 == i2:
                                path = merge_paths(beg_path, end_path)
                            else:
                                path = self._find_path_between_chains(i1, i2)
                                path = merge_paths(beg_path, path, end_path)
                            if len(path) < len(shortest_path):
                                shortest_path = path
            shortest_path = finalize_path(shortest_path)

        return shortest_path
