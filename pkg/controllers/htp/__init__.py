import sys

from pkg.controllers import BaseController
from pkg.controllers.htp.response import HtpResponse
from pkg.models.board import Board
from pkg.views.string_board_view import StringBoardView


class HtpController(BaseController):
    _board: Board = None

    def run(self):
        for line in sys.stdin:
            cmd = line.strip('\n')
            if cmd == 'name':
                resp = HtpResponse('PyHex')
            elif cmd == 'version':
                resp = HtpResponse('0.0.1')
            elif cmd == 'hexgui-analyze_commands':
                resp = HtpResponse()
            elif cmd == 'showboard':
                resp = HtpResponse(self._view.render())
            elif cmd.startswith('boardsize'):
                self._board = Board(11, 11)
                self._view.set_board(self._board)
                self._ai.set_board(self._board)
                resp = HtpResponse()
            elif cmd.startswith('play'):
                resp = HtpResponse()
            elif cmd.startswith('genmove'):
                resp = HtpResponse()
            else:
                resp = HtpResponse(error=f'unknown command: {cmd}')
            resp.do()
