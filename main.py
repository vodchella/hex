from pkg.constants.game import PLAYER_ONE, PLAYER_TWO
from pkg.models.board import Board
from pkg.views.console_board_view import ConsoleBoardView

if __name__ == '__main__':
    board = Board(3, 3)
    board.set_cell_by_xy(1, 1, PLAYER_TWO)
    board.set_cell_by_xy(2, 1, PLAYER_TWO)
    board.set_cell_by_xy(3, 1, PLAYER_TWO)

    copied_board = board.copy()
    copied_board.set_cell_by_xy(3, 3, PLAYER_ONE)

    c_view = ConsoleBoardView(board)
    c_view.render()
    c_view.set_board(copied_board)
    c_view.render()
