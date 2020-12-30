from functools import reduce
from pkg.ai.pathfinders import Node, INFINITY, to_nodes
from pkg.ai.pathfinders.astar import AStarPathfinder
from pkg.ai.pathfinders.basic import BasicPathfinder
from pkg.ai.pathfinders.walker import WalkerPathfinder
from pkg.constants.game import PLAYER_NONE, PLAYER_ONE, PLAYER_TWO
from pkg.ai.pathfinders.utils.paths import merge_paths


SHORTEST_PATH_LENGTH_TO_ANALYZE = 3


class ChainPathfinder(BasicPathfinder):
    _astar: AStarPathfinder = None
    _for_player = None
    _opponent = None
    _dst_node = None
    _chains = []
    _chain_paths = []

    def __init__(self, board):
        super().__init__(board)

    def _init_vars(self, to_node: Node, for_player):
        self._dst_node = to_node
        self._for_player = for_player
        self._opponent = PLAYER_ONE if self._for_player == PLAYER_TWO else PLAYER_TWO

    def _init_data(self):
        self._astar = AStarPathfinder(self._board)
        self._chains = [(i, c) for i, c in enumerate(self._find_chains())]
        self._chain_paths = self._find_paths_between_all_chains()

    def _find_chains(self):
        result = []
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
                            cells = board.get_cell_neighbors(node.x(), node.y(), [self._opponent, PLAYER_NONE])
                            new_reachable = [n for n in filter(lambda n: n not in explored, to_nodes(cells))]
                            for adjacent in new_reachable:
                                if adjacent not in reachable:
                                    reachable.append(adjacent)
                        if len(chain):
                            result.append(chain)
        return result

    def _find_paths_between_all_chains(self):
        paths = []

        def find_path(i1, i2):
            result = [p for p in filter(lambda p: p[0] == i1 and p[1] == i2, paths)]
            return result[0] if len(result) > 0 else None

        if len(self._chains) > 1:
            for (i, chain_from) in self._chains:
                for (j, chain_to) in self._chains:
                    existing_path = find_path(j, i)
                    if existing_path:
                        paths.append((i, j, existing_path[2], existing_path[3], existing_path[4]))
                    else:
                        path, node_from, node_to = self._find_path_between_two_chains(chain_from, chain_to)
                        if len(path):
                            paths.append((i, j, path, node_from, node_to))
        return paths

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
        for to_chain_node in to_chain:
            path = self._astar.find_path(
                self._for_player,
                from_node.x(),
                from_node.y(),
                to_chain_node.x(),
                to_chain_node.y()
            )
            path_len = len(path)
            if path_len == 0:
                break
            if path_len < shortest_path_len:
                shortest_path_len = path_len
                shortest_path = path
                best_node = to_chain_node
            elif path_len == shortest_path_len:
                path_to_dst = self._astar.find_path(
                    self._for_player,
                    to_chain_node.x(),
                    to_chain_node.y(),
                    self._dst_node.x(),
                    self._dst_node.y()
                )
                path_to_dst_len = len(path_to_dst)
                if path_to_dst_len > 0:
                    if path_to_dst_len < shortest_path_to_dst_len:
                        shortest_path_to_dst_len = path_to_dst_len
                        shortest_path_len = path_len
                        shortest_path = path
                        best_node = to_chain_node

        return shortest_path[1:-1], best_node

    def _find_path_between_chains(self, src_chain_id: int, dst_chain_id: int):
        visited_ids = []

        def recursive(c_path):
            visited_ids.append(c_path[0])
            if c_path[1] == dst_chain_id:
                return [c_path]
            else:
                r = [c_path]
                s_paths = [p for p in filter(
                    lambda cp: cp[0] == c_path[1] and cp[1] not in visited_ids, self._chain_paths
                )]
                for sp in s_paths:
                    r += recursive(sp)
                return r

        shortest_path_len = INFINITY
        shortest_path = []
        starting_paths = [p for p in filter(lambda cp: cp[0] == src_chain_id, self._chain_paths)]
        for chain_path in starting_paths:
            visited_ids = []
            path = recursive(chain_path)
            do_reduce = len(path) > 1
            path_len = reduce(lambda a, b: len(a[2]) + len(b[2]), path) if do_reduce else len(path[0][2])
            if path_len < shortest_path_len:
                shortest_path_len = path_len
                shortest_path = reduce(lambda a, b: a[2] + b[2], path) if do_reduce else path[0][2]

        return shortest_path

    def _find_path(self, from_node: Node, to_node: Node):
        def is_free_cell(cell):
            return self._board.get_cell(cell[0], cell[1]) == PLAYER_NONE

        def finalize_path(path_to_finalize):
            beg = from_node.tuple()
            end = to_node.tuple()
            beg_p = [beg] if is_free_cell(beg) else []
            end_p = [end] if is_free_cell(end) else []
            return merge_paths(beg_p, path_to_finalize, end_p)

        shortest_path = self._astar.find_path(self._for_player, from_node.x(), from_node.y(), to_node.x(), to_node.y())
        shortest_path = [p for p in filter(lambda c: is_free_cell(c), shortest_path)]

        if len(shortest_path) >= SHORTEST_PATH_LENGTH_TO_ANALYZE:
            for i1, chain1 in self._chains:
                beg_path, n1 = self._find_path_from_node_to_chain(from_node, chain1)
                if n1 is not None:
                    for i2, chain2 in self._chains:
                        end_path, n2 = self._find_path_from_node_to_chain(to_node, chain2)
                        if n2 is not None:
                            mid_path = self._find_path_between_chains(i1, i2) if i1 != i2 else []
                            path = finalize_path(merge_paths(beg_path, mid_path, end_path))
                            if len(path) < len(shortest_path):
                                shortest_path = path

        return shortest_path

    def _construct_full_path(self, src: Node, dst: Node, path):
        board = self._board.copy(check_bounds=False)
        board.set_cells(path, self._for_player)
        walker = WalkerPathfinder(board)
        return walker.find_path(self._for_player, src.x(), src.y(), dst.x(), dst.y())

    def find_path(self, for_player, src_x, src_y, dst_x, dst_y):
        def cell_is_not_src_or_dst(cell):
            node = Node(cell[0], cell[1])
            return node != from_node and node != to_node

        from_node = Node(src_x, src_y)
        to_node = Node(dst_x, dst_y)
        self._init_vars(to_node, for_player)
        self._init_data()

        shortest_path = self._find_path(from_node, to_node)
        shortest_path_len = len(shortest_path)
        if shortest_path_len >= SHORTEST_PATH_LENGTH_TO_ANALYZE:
            shortest_full_path = self._construct_full_path(from_node, to_node, shortest_path)
            shortest_full_path_len = len(shortest_full_path)

            while True:
                found = False
                path_without_src_and_dst = [p for p in filter(lambda c: cell_is_not_src_or_dst(c), shortest_path)]
                new_board = self._board.copy(check_bounds=False)
                new_board.set_cells(path_without_src_and_dst, self._opponent)
                self._board = new_board
                self._init_data()
                verifiable_path = self._find_path(from_node, to_node)
                verifiable_path_len = len(verifiable_path)
                if verifiable_path_len == shortest_path_len:
                    verifiable_full_path = self._construct_full_path(from_node, to_node, verifiable_path)
                    verifiable_full_path_len = len(verifiable_full_path)
                    if verifiable_full_path_len < shortest_full_path_len:
                        shortest_path = verifiable_path
                        shortest_full_path_len = verifiable_full_path_len
                        found = True
                if not found:
                    break

        return shortest_path
