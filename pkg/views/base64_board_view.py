from pkg.models.board import Board


class Base64BoardView:
    _board: Board = None

    def __init__(self, board):
        self._board = board

    def render(self):
        if self._board:
            board_size = self._board.get_size()
            result = []
            byte = 0

            for (i, cell) in enumerate(self._board.get_cells(), start=1):
                cells_left = i % 4
                byte_completed = cells_left == 0

                byte += cell
                if not byte_completed:
                    byte = byte << 2

                if byte_completed and i > 1:
                    print(bin(byte))
                    result.append(byte)
                    byte = 0

                if i == board_size and not byte_completed:
                    byte = byte << (2 * (4 - cells_left - 1))
                    print(bin(byte))
                    result.append(byte)
