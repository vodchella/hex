from pkg.constants.game import PLAYER_ONE, PLAYER_TWO, PLAYER_NONE
from pkg.loaders.binary_board_loader import BinaryBoardLoader
from pkg.models.board import Board
from pkg.views.binary_board_view import BinaryBoardView
from pkg.views.console_board_view import ConsoleBoardView

if __name__ == '__main__':
    board = Board(5, 6)
    board.set_cell_by_xy(1, 1, PLAYER_TWO)
    board.set_cell_by_xy(2, 1, PLAYER_TWO)
    board.set_cell_by_xy(3, 1, PLAYER_TWO)
    board.set_cell_by_xy(1, 3, PLAYER_TWO)
    board.set_cell_by_xy(2, 3, PLAYER_NONE)
    board.set_cell_by_xy(3, 3, PLAYER_ONE)
    board.set_cell_by_xy(4, 6, PLAYER_ONE)
    board.set_cell_by_xy(5, 6, PLAYER_TWO)

    c_view = ConsoleBoardView(board)
    c_view.render()

    b_view = BinaryBoardView(board)
    data = b_view.render()
    print(data)

    loaded_board = BinaryBoardLoader.load(data)
    c_view = ConsoleBoardView(loaded_board)
    c_view.render()
