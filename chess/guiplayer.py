
from . import player

class GUIPlayer(player.Player):
    
    def take_turn(self, move):
        self.controller.take_turn(move)
