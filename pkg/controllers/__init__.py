from pkg.ai import BaseAI
from pkg.views import BaseBoardView


class BaseController:
    _ai: BaseAI = None
    _view: BaseBoardView = None

    def __init__(self, ai: BaseAI, view: BaseBoardView):
        self._ai = ai
        self._view = view

    def run(self):
        pass
