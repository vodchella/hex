from pkg.ai.pathfinders.astar import AStarPathfinder


class WalkerPathfinder(AStarPathfinder):
    def __init__(self, board):
        super().__init__(board, walk_only_by_own_cells=True)
