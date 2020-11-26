from pkg.models.board import Board


class AStar:
    _board: Board = None

    def __init__(self, board):
        self.set_board(board)

    def set_board(self, board):
        self._board = board

    def find_path(self, for_player, src_x, src_y, dst_x, dst_y):
        pass
