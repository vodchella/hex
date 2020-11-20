from pkg.constants.game import PLAYER_NONE
from pkg.exceptions.board import BoardDimensionsException, BoardIndexOutOfBounds, BoardCoordinateOutOfBounds

BOARD_MAX_SIZE = 11


class Board:
    _width: int = 0
    _height: int = 0
    _cells = []

    def __init__(self, width, height, cells=None):
        if not cells:
            if width < 1 or height < 1:
                raise BoardDimensionsException('Board size can\'t be less than one')
            if width > BOARD_MAX_SIZE or height > BOARD_MAX_SIZE:
                raise BoardDimensionsException('Board size can\'t be greater than eleven')

        self._width = width
        self._height = height
        self._cells = cells if cells else [PLAYER_NONE] * width * height

    def _check_board_index(self, index):
        if index < 0 or index > len(self._cells) - 1:
            raise BoardIndexOutOfBounds(f'Index {index} is out of board bounds')

    def _get_index_from_xy(self, x, y):
        if x > BOARD_MAX_SIZE or y > BOARD_MAX_SIZE:
            coord = x if x > y else y
            raise BoardCoordinateOutOfBounds(f'Coordinate {coord} is out of board bounds')
        return (y - 1) * self._width + (x - 1)

    def get_dimensions(self):
        return self._width, self._height

    def get_size(self):
        return len(self._cells)

    def get_cells(self):
        return self._cells

    def get_cell_by_xy(self, x, y):
        return self._cells[self._get_index_from_xy(x, y)]

    def set_cell_by_xy(self, x, y, player):
        self._cells[self._get_index_from_xy(x, y)] = player

    def get_cell_by_index(self, index):
        self._check_board_index(index)
        return self._cells[index]

    def set_cell_by_index(self, index, player):
        self._check_board_index(index)
        self._cells[index] = player

    def copy(self):
        copied_cells = self._cells.copy()
        return Board(self._width, self._height, copied_cells)
