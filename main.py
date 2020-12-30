#!/usr/bin/env python3

from pkg.ai.default import DefaultAI
from pkg.controllers.htp import HtpController
from pkg.views import BaseBoardView

if __name__ == '__main__':
    ai = DefaultAI()
    view = BaseBoardView()
    ctrl = HtpController(ai, view)
    ctrl.run()
