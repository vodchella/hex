from pkg.ai import BaseAI


class DefaultAI(BaseAI):
    def find_move(self, for_player):
        return 'a1'
