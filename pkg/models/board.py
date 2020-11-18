class Board:
    _width: int = 0
    _height: int = 0
    _cells = []

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._cells = [0] * width * height

    def _get_index_from_xy(self, x, y):
        return (y - 1) * self._width + (x - 1)

    def get_dimensions(self):
        return self._width, self._height

    def get_cell_xy(self, x, y):
        return self._cells[self._get_index_from_xy(x, y)]

    def set_cell_xy(self, x, y, player):
        self._cells[self._get_index_from_xy(x, y)] = player
