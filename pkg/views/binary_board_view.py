from pkg.models.board import Board

CELLS_IN_BYTE = 4
BITS_PER_CELL = 2


class BinaryBoardView:
    _board: Board = None

    def __init__(self, board):
        self._board = board

    def render(self):
        if self._board:
            board_size = self._board.get_size()
            result = []
            byte = 0

            for (i, cell) in enumerate(self._board.get_cells(), start=1):
                cells_left = i % CELLS_IN_BYTE
                byte_completed = cells_left == 0

                byte += cell
                if not byte_completed:
                    byte = byte << BITS_PER_CELL

                if byte_completed and i > 1:
                    result.append(byte)
                    byte = 0

                if i == board_size and not byte_completed:
                    byte = byte << (BITS_PER_CELL * (CELLS_IN_BYTE - cells_left - 1))
                    result.append(byte)

            while len(result):
                if result[-1]:
                    break
                else:
                    result.pop()

            return result
