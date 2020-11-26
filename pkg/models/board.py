from pkg.constants.game import PLAYER_NONE
from pkg.exceptions.board import BoardDimensionsException, BoardIndexOutOfBounds, BoardCoordinateOutOfBounds

BOARD_MAX_SIZE = 11

DIRECTIONS = [
    (+0, -1),  # top left
    (+1, -1),  # top right
    (+1, +0),  # right
    (+0, +1),  # bottom right
    (-1, +1),  # bottom left
    (-1, +0),  # left
]


class Board:
    _check_bounds: bool = True
    _width: int = 0
    _height: int = 0
    _max_x: int = 0
    _max_y: int = 0
    _cells = []

    def __init__(self, width, height, check_bounds=True, cells=None):
        if check_bounds:
            if width < 1 or height < 1:
                raise BoardDimensionsException('Board size can\'t be less than one')
            if width > BOARD_MAX_SIZE or height > BOARD_MAX_SIZE:
                raise BoardDimensionsException('Board size can\'t be greater than eleven')
            if cells and len(cells) != width * height:
                raise BoardDimensionsException('Board size doesn\'t match to cells array')

        self._check_bounds = check_bounds
        self._width = width
        self._height = height
        self._max_x = width - 1
        self._max_y = height - 1
        self._cells = cells if cells else [PLAYER_NONE] * width * height

    def _is_index_valid(self, index):
        return 0 <= index < len(self._cells)

    def _is_xy_valid(self, x, y):
        return (0 <= x <= self._max_x) and (0 <= y <= self._max_y)

    def _check_board_index(self, index):
        if not self._is_index_valid(index):
            raise BoardIndexOutOfBounds(f'Index {index} is out of board bounds')

    def _check_board_xy(self, x, y):
        if not self._is_xy_valid(x, y):
            raise BoardCoordinateOutOfBounds(f'Coordinates {x}, {y} is out of board bounds')

    def _get_index_from_xy(self, x, y):
        if self._check_bounds:
            self._check_board_xy(x, y)
        return y * self._width + x

    def _get_xy_from_index(self, index):
        if self._check_bounds:
            self._check_board_index(index)
        y, x = divmod(index, self._width)
        return x, y

    def get_dimensions(self):
        return self._width, self._height

    def get_size(self):
        return len(self._cells)

    def get_cells(self):
        return self._cells

    def get_cell(self, x, y):
        return self._cells[self._get_index_from_xy(x, y)]

    def set_cell(self, x, y, player):
        self._cells[self._get_index_from_xy(x, y)] = player

    def get_cell_by_index(self, index):
        self._check_board_index(index)
        return self._cells[index]

    def set_cell_by_index(self, index, player):
        self._check_board_index(index)
        self._cells[index] = player

    def get_cell_neighbors(self, x, y, exclude_players=None):
        if self._check_bounds:
            self._check_board_xy(x, y)

        result = []
        for d in DIRECTIONS:
            nx = x + d[0]
            ny = y + d[1]

            append = False
            if self._is_xy_valid(nx, ny):
                if exclude_players:
                    player = self.get_cell(nx, ny)
                    if player not in exclude_players:
                        append = True
                else:
                    append = True

            if append:
                result.append((nx, ny))

        return result

    def copy(self, check_bounds=True):
        if self._cells:
            copied_cells = self._cells.copy()
            return Board(
                self._width,
                self._height,
                check_bounds=check_bounds,
                cells=copied_cells
            )
