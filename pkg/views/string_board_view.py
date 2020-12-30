from pkg.views import BaseBoardView

PLAYER_CHARS = [' ', 'O', '*', '-']


def char(player):
    return PLAYER_CHARS[player]


class StringBoardView(BaseBoardView):
    _for_hexgui: bool = False

    def __init__(self, board=None, for_hexgui=False):
        super().__init__(board)
        self._for_hexgui = for_hexgui

    def render(self):
        result = ['Board:'] if self._for_hexgui is True else []
        if self._board:
            w, h = self._board.get_dimensions()

            ord_of_a = ord('A')
            symbol_coordinates = ' ' + ''.join(['   ' + chr(c + ord_of_a) for c in range(w)])
            result.append(symbol_coordinates)

            topping_of_top_cells = '  ' + ''.join([' / \\' for _ in range(w)])
            result.append(topping_of_top_cells)

            for y in range(h):
                indent = y * '  ' if y < 9 else (y - 1) * '  ' + ' '
                side_coord = str(y + 1)

                cells_center = indent + side_coord + ' '
                cells_center += ''.join(['| ' + char(self._board.get_cell(i, y)) + ' ' for i in range(w)])
                cells_center += '| ' + side_coord
                result.append(cells_center)

                cells_bottom = indent + ('  ' if y < 9 else '   ') + ''.join([' \\ /' for _ in range(w)])
                cells_bottom += ' \\' if y < (h - 1) else ''
                result.append(cells_bottom)

            result.append('  ' * (h - 1) + symbol_coordinates)
        return '\n'.join(result)
