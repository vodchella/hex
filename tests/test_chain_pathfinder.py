from pkg.ai.pathfinders.chain import ChainPathfinder
from pkg.constants.game import PLAYER_ONE, PLAYER_TWO, PLAYER_NONE
from pkg.models.board import Board
from pkg.utils.paths import compare_paths


def _init_test_board():
    board = Board(7, 7)

    board.set_cell(3, 0, PLAYER_ONE)
    board.set_cell(2, 1, PLAYER_ONE)
    board.set_cell(1, 3, PLAYER_ONE)
    board.set_cell(1, 4, PLAYER_ONE)
    board.set_cell(2, 4, PLAYER_ONE)
    board.set_cell(3, 5, PLAYER_ONE)
    board.set_cell(3, 6, PLAYER_ONE)
    board.set_cell(4, 6, PLAYER_ONE)
    board.set_cell(5, 6, PLAYER_ONE)

    board.set_cell(0, 6, PLAYER_ONE)
    board.set_cell(0, 5, PLAYER_TWO)
    board.set_cell(1, 5, PLAYER_TWO)
    board.set_cell(1, 6, PLAYER_TWO)

    board.set_cell(5, 2, PLAYER_TWO)
    board.set_cell(6, 2, PLAYER_TWO)

    board.set_cell(2, 2, PLAYER_TWO)
    board.set_cell(1, 2, PLAYER_TWO)

    return board


class TestChainPathfinder:
    def test_1(self):
        pf = ChainPathfinder(_init_test_board())
        path = pf.find_path(PLAYER_ONE, 6, 0, 6, 6)

        assert compare_paths(
            path,
            [(6, 0), (4, 4), (4, 3), (4, 2), (5, 1), (6, 6)]
        )

    def test_2(self):
        board = _init_test_board()
        board.set_cell(4, 0, PLAYER_ONE)
        board.set_cell(1, 2, PLAYER_NONE)

        pf = ChainPathfinder(board)
        path = pf.find_path(PLAYER_ONE, 6, 0, 6, 6)

        assert compare_paths(
            path,
            [(6, 0), (5, 0), (1, 2), (3, 4), (6, 6)]
        )

    def test_3(self):
        board = Board(3, 3)
        board.set_cell(0, 1, PLAYER_TWO)
        board.set_cell(1, 1, PLAYER_TWO)
        board.set_cell(2, 1, PLAYER_TWO)

        pf = ChainPathfinder(board)
        path = pf.find_path(PLAYER_ONE, 0, 0, 2, 2)

        assert len(path) == 0

    def test_4(self):
        board = Board(7, 7)
        board.set_cell(5, 1, PLAYER_ONE)
        board.set_cell(4, 2, PLAYER_ONE)
        board.set_cell(6, 5, PLAYER_ONE)
        board.set_cell(5, 5, PLAYER_ONE)
        board.set_cell(4, 5, PLAYER_ONE)
        board.set_cell(3, 5, PLAYER_ONE)
        board.set_cell(2, 5, PLAYER_ONE)
        board.set_cell(1, 5, PLAYER_ONE)

        pf = ChainPathfinder(board)
        path = pf.find_path(PLAYER_ONE, 6, 0, 6, 6)

        assert compare_paths(
            path,
            [(6, 0), (4, 4), (4, 3), (6, 6)]
        )

    def test_5(self):
        board = Board(7, 7)
        board.set_cell(5, 3, PLAYER_ONE)
        board.set_cell(6, 3, PLAYER_ONE)
        board.set_cell(6, 4, PLAYER_ONE)

        pf = ChainPathfinder(board)
        path = pf.find_path(PLAYER_ONE, 6, 0, 6, 6)

        assert compare_paths(
            path,
            [(6, 0), (6, 2), (6, 1), (6, 5), (6, 6)]
        )

    def test_6(self):
        board = Board(7, 7)
        board.set_cell(3, 0, PLAYER_ONE)
        board.set_cell(4, 0, PLAYER_ONE)
        board.set_cell(5, 1, PLAYER_ONE)
        board.set_cell(5, 2, PLAYER_ONE)
        board.set_cell(6, 3, PLAYER_ONE)
        board.set_cell(6, 4, PLAYER_ONE)

        pf = ChainPathfinder(board)
        path = pf.find_path(PLAYER_ONE, 0, 0, 6, 6)

        assert compare_paths(
            path,
            [(0, 0), (2, 0), (1, 0), (5, 0), (6, 2), (6, 5), (6, 6)]
        )
