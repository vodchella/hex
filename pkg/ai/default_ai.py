from pkg.models.board import Board


class DefaultAI:
    _board: Board = None

    def __init__(self, board):
        self.set_board(board)

    def set_board(self, board):
        self._board = board

    def find_move(self, for_player):
        pass
