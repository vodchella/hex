from pkg.models.board import Board


class BinaryBoardLoader:
    @staticmethod
    def load(data):
        dim_byte = data[0]
        h = dim_byte & 0b00001111
        w = dim_byte >> 4
        result = Board(w, h)

        return result
