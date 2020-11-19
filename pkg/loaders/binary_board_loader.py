from pkg.exceptions.board import BoardIndexOutOfBounds
from pkg.models.board import Board


class BinaryBoardLoader:
    @staticmethod
    def load(data):
        dim_byte = data.pop(0)
        h = dim_byte & 0b00001111
        w = dim_byte >> 4
        result = Board(w, h)

        for (i, byte) in enumerate(data):
            cell_1 = (byte & 0b11000000) >> 6
            cell_2 = (byte & 0b00110000) >> 4
            cell_3 = (byte & 0b00001100) >> 2
            cell_4 = (byte & 0b00000011)

            shift = i * 4
            try:
                result.set_cell_by_index(0 + shift, cell_1)
                result.set_cell_by_index(1 + shift, cell_2)
                result.set_cell_by_index(2 + shift, cell_3)
                result.set_cell_by_index(3 + shift, cell_4)
            except BoardIndexOutOfBounds:
                # Do nothing because board is ended
                pass

        return result
