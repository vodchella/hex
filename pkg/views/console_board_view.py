from pkg.models.board import Board

PLAYER_CHARS = [' ', '*', 'O']


def char(player):
    return PLAYER_CHARS[player]


class ConsoleBoardView:
    _board: Board = None

    def __init__(self, board):
        self.set_board(board)

    def set_board(self, board):
        self._board = board

    def render(self):
        if self._board:
            w, h = self._board.get_dimensions()

            ord_of_a = ord('A')
            symbol_coordinates = ' ' + ''.join(['   ' + chr(c + ord_of_a) for c in range(w)])
            print(symbol_coordinates)

            topping_of_top_cells = '  ' + ''.join([' / \\' for _ in range(w)])
            print(topping_of_top_cells)

            for y in range(h):
                y_index = y + 1
                indent = y * '  ' if y < 9 else (y - 1) * '  ' + ' '
                side_coord = str(y_index)

                cells_center = indent + side_coord + ' '
                cells_center += ''.join(['| ' + char(self._board.get_cell_by_xy(i + 1, y_index)) + ' ' for i in range(w)])
                cells_center += '| ' + side_coord
                print(cells_center)

                cells_bottom = indent + ('  ' if y < 9 else '   ') + ''.join([' \\ /' for _ in range(w)])
                cells_bottom += ' \\' if y_index < h else ''
                print(cells_bottom)

            print('  ' * (h - 1) + symbol_coordinates)
