from pkg.views import BaseBoardView
from pkg.views.string_board_view import StringBoardView


class ConsoleBoardView(BaseBoardView):
    def render(self):
        if self._board:
            sbv = StringBoardView(self._board)
            print(sbv.render())
