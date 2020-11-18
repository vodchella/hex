from pkg.constants.game import PLAYER_ONE, PLAYER_TWO
from pkg.models.board import Board
from pkg.views.console_board_view import ConsoleBoardView

if __name__ == '__main__':
    board = Board(3, 3)
    board.set_cell_xy(2, 2, PLAYER_ONE)
    board.set_cell_xy(3, 3, PLAYER_TWO)
    view = ConsoleBoardView(board)
    view.render()
