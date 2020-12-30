from pkg.constants.game import PLAYER_NONE, PLAYER_VIRTUAL
from pkg.views import BaseBoardView

CELLS_IN_BYTE = 4
BITS_PER_CELL = 2


class BinaryBoardView(BaseBoardView):
    def render(self):
        if self._board:
            w, h = self._board.get_dimensions()
            dim_byte = w
            dim_byte = dim_byte << 4
            dim_byte += h
            result = [dim_byte]

            board_size = self._board.get_size()
            byte = 0

            for (i, cell) in enumerate(self._board.get_cells(), start=1):
                cells_left = i % CELLS_IN_BYTE
                byte_completed = cells_left == 0

                byte += cell if cell != PLAYER_VIRTUAL else PLAYER_NONE
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
