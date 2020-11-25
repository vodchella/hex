from pkg.constants.game import PLAYER_ONE, PLAYER_TWO
from pkg.models.board import Board
from pkg.views.console_board_view import ConsoleBoardView

if __name__ == '__main__':
    board = Board(3, 3)
    board.set_cell_by_xy(2, 0, PLAYER_ONE)

    neighbors = board.get_cell_neighbors_by_xy(2, 0)
    for n in neighbors:
        board.set_cell_by_xy(n[0], n[1], PLAYER_TWO)

    c_view = ConsoleBoardView(board)
    c_view.render()
