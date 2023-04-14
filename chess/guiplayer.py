
from . import player

class GUIPlayer(player.Player):
    
    def take_turn(self, move):
        return self.controller.take_turn(move)
