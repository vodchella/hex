#!/usr/bin/env python3

import sys
from pkg.ai.default import DefaultAI
from pkg.controllers.htp import HtpController
from pkg.utils.console import panic
from pkg.views.string_board_view import StringBoardView

if __name__ == '__main__':
    if sys.version_info < (3, 8):
        panic('We need minimum Python version 3.8 to run. Current version: %s.%s.%s' % sys.version_info[:3])

    ai = DefaultAI()
    view = StringBoardView(for_hexgui=True)
    ctrl = HtpController(ai, view)
    ctrl.run()
