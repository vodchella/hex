from pkg.models.board import Board


class BaseAI:
    _board: Board = None

    def __init__(self, board=None):
        if board is not None:
            self.set_board(board)

    def set_board(self, board):
        self._board = board

    def find_move(self, for_player):
        pass
