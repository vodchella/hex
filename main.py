from pkg.constants.game import PLAYER_ONE, PLAYER_TWO, PLAYER_NONE
from pkg.models.board import Board
from pkg.views.binary_board_view import BinaryBoardView
from pkg.views.console_board_view import ConsoleBoardView

if __name__ == '__main__':
    board = Board(3, 3)
    board.set_cell_xy(1, 1, PLAYER_TWO)
    board.set_cell_xy(2, 1, PLAYER_TWO)
    board.set_cell_xy(3, 1, PLAYER_TWO)
    board.set_cell_xy(1, 2, PLAYER_TWO)
    board.set_cell_xy(2, 2, PLAYER_NONE)
    board.set_cell_xy(3, 2, PLAYER_ONE)
    # board.set_cell_xy(1, 3, PLAYER_ONE)
    # board.set_cell_xy(2, 3, PLAYER_TWO)
    # board.set_cell_xy(3, 3, PLAYER_TWO)

    c_view = ConsoleBoardView(board)
    c_view.render()

    b_view = BinaryBoardView(board)
    print(b_view.render())
