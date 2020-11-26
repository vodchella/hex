from pkg.ai.pathfinders.astar import AStar
from pkg.constants.game import PLAYER_ONE, PLAYER_TWO
from pkg.models.board import Board
from pkg.views.console_board_view import ConsoleBoardView

if __name__ == '__main__':
    board = Board(3, 3)
    board.set_cell(0, 1, PLAYER_TWO)

    c_view = ConsoleBoardView(board)
    c_view.render()

    pf = AStar(board)
    pf.find_path(PLAYER_ONE, 0, 0, 0, 2)
