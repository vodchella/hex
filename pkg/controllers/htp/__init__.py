import sys
from pkg.constants.version import APP_NAME, APP_VERSION_FULL
from pkg.controllers import BaseController
from pkg.controllers.htp.response import HtpResponse
from pkg.models.board import Board
from pkg.utils import bye


class HtpController(BaseController):
    _board: Board = None

    def run(self):
        for line in sys.stdin:
            cmd = line.strip('\n')
            if cmd == 'name':
                resp = HtpResponse(APP_NAME)
            elif cmd == 'version':
                resp = HtpResponse(APP_VERSION_FULL)
            elif cmd == 'hexgui-analyze_commands':
                resp = HtpResponse()
            elif cmd == 'quit':
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
            if cmd == 'quit':
                bye()
