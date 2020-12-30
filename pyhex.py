#!/usr/bin/env python3

from pkg.ai.default import DefaultAI
from pkg.controllers.htp import HtpController
from pkg.views.string_board_view import StringBoardView

if __name__ == '__main__':
    ai = DefaultAI()
    view = StringBoardView(for_hexgui=True)
    ctrl = HtpController(ai, view)
    ctrl.run()
